"""
A module that implements the CameraMonitor class.
"""

import threading
from datetime import datetime
import time
import logging

import cv2

from vigi.utils.fps_calculator import FPSCalculator
from .utils.pub_sub import PubSub
from .database import Database


class CameraMonitor(threading.Thread):
    """
    A class that monitors one camera for motion.
    """

    def __init__(self, video_recorder = None, camera_id=0, max_errors=50,
                 add_seconds_after_motion=10, notifier=None, db_path=None,
                 motion_detector=None):
        """
        max_errors: int - the maximum number of consecutive errors when reading
                            a frame from the camera before the camera monitor stops.
                            It's used to prevent the camera monitor from creating
                            a big number of small recordings on each small motion.
        add_seconds_after_motion: int - the number of seconds to add to the
                            video after the motion is detected
        notifier: Notifier - a notifier object to send notifications about the motion
        db_path: str - the path to the database file
        """
        super().__init__()

        self.notifier = notifier

        self.camera_id = camera_id
        self.max_errors = max_errors
        self.add_seconds_after_motion = add_seconds_after_motion

        # Initialize the PubSub object to stream the frames from the camera
        # so other parts of the application can access the stream of frames
        self.frame_stream = PubSub()

        self.motion_detector = motion_detector

        # when motion is detected, the motion_callback will be called
        self.motion_detector.set_motion_callback(self.motion_callback)

        # video_recorder is used to save the video to a file when motion is detected
        self.video_recorder = video_recorder

        # save the start time of the camera monitor to calculate the uptime
        self.start_time = datetime.now()

        self.fps_calculator = FPSCalculator(max_history_size=50)

        # number of frames to add after the motion is over,
        # initially it's set to 0, but it could be assigned a value when the motion is detected
        # and decremented in each frame until it reaches 0
        self.add_frames = 0

        # A flag to stop the camera monitor
        self.should_stop = False

        # A set of detected objects during the recording
        self.detected_objects = set()

        # we can't initialize the database here, because the database should be initialized in
        # the same thread where it's used, but __init__ is called in the main thread
        self.db_path = db_path

        # the database connection, it will be initialized in the run method
        self.database = None

        # camera parameters, they will be initialized in the run method
        self.frame_width = None
        self.frame_height = None
        self.camera_fps = None

    def current_fps(self):
        """
        Returns the current FPS of the system using the FPS calculator if it has calculated the FPS,
        otherwise returns the FPS of the camera.
        """
        fps = self.fps_calculator.current_fps()
        logging.info("Calculated FPS = %s", fps)
        if fps is None:
            fps = int(self.camera_fps)
            logging.warning("FPS is not calculated yet, using the camera's FPS = %s", fps)

        if fps == 1:
            logging.warning("The camera's FPS is 1, it seems to be invalid."
                            "Setting the default FPS to 30.")
            fps = 30

        return fps

    def motion_callback(self):
        """
        This function is called when motion is detected by the motion detector.
        """
        logging.info("Motion detected!")

        # send a notification about the motion
        self.notifier.notify(f"Motion was detected by the camera #{self.camera_id}")

        self.add_frames = self.add_seconds_after_motion * self.current_fps()

        if self.video_recorder.is_recording():
            logging.info("Motion detected while the video is being recorded.")
            return

        # reset the set of detected objects
        self.detected_objects = set()

        # We need to determine the FPS of the camera to pass it to the video recorder
        # as FPS will be saved as metadata in the video file
        # if FPS will be overestimated, the video will be played faster than it should be
        # if FPS will be underestimated, the video will be played slower than it should be
        # Start recording the video:
        self.video_recorder.start_recording(frame_width=self.frame_width,
                                            frame_height=self.frame_height,
                                            fps=self.current_fps())

    def run(self):
        # Connect to the database. We need to connect to the database in the same
        # thread where it's used
        self.database = Database(self.db_path)

        # Initialize the camera with OpenCV
        logging.info("Starting camera monitor... ")
        camera = cv2.VideoCapture(self.camera_id)  # Use 0 for the first webcam
        if camera.isOpened():
            logging.info("Camera opened successfully.")
        else:
            logging.error("Camera with ID=%s could not be opened.", self.camera_id)
            return

        try:
            self.frame_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.frame_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.camera_fps = camera.get(cv2.CAP_PROP_FPS)
            logging.info("Camera parameters: "
                         "frame width: %s, frame height: %s, FPS: %s",
                         self.frame_width, self.frame_height, self.camera_fps)

            error_count = 0
            while not self.should_stop:
                success, frame = camera.read()  # Read a frame from the camera
                if not success:
                    # If the camera fails to read a frame:
                    # - Increment the error count
                    # - Print an error message
                    # - Sleep for 1 second
                    #
                    # If the error count reaches the maximum number of consecutive errors:
                    # - print an error message and break the loop

                    error_count += 1
                    if error_count >= self.max_errors:
                        logging.fatal("Maximum number of consecutive errors (%s) reached. "
                                      "Exiting.", self.max_errors)
                        break

                    logging.error("Failed to read a frame from the camera with ID=%s",
                                  self.camera_id)
                    time.sleep(1)
                    continue

                # Reset the error count if a frame is successfully read
                error_count = 0

                # Apply the motion detector to the frame
                frame, detected_objects = self.motion_detector.update(frame)

                # Add the detected objects to the set of detected objects
                self.detected_objects.update(detected_objects)

                # Publish the frame to the frame stream
                self.frame_stream.publish(frame)

                # if motion is not detected anymore and the video is being recorded, then
                # stop the recording
                if not self.motion_detector.is_motion_detected() and \
                        self.video_recorder.is_recording():
                    self.add_frames -= 1
                    if self.add_frames <= 0:
                        self.end_recording()

                # here we send all frames to the video recorder, it's up to the
                # video recorder to decide if it should record the frame or not.
                # It could decide to record additional frames before and after
                # the motion is detected
                self.video_recorder.add_frame(frame)
                self.fps_calculator.update()

        finally:
            if self.video_recorder.is_recording():
                self.end_recording()

            # OpenCV cleanup
            logging.info("Releasing the camera...")
            camera.release()

            # close the database connection to save the data
            self.database.close()

    def end_recording(self):
        """
        End the recording of the video to a file.
        """
        self.database.add_recording(date=self.video_recorder.recording_start_date,
                                    time=self.video_recorder.recording_start_time,
                                    camera_id=self.camera_id, tags=','.join(self.detected_objects))

        # send a notification about the detected objects
        message = f"Moving objects detected: {', '.join(self.detected_objects)} " \
                   "by the camera #{self.camera_id}"
        self.notifier.notify(message)

        self.video_recorder.end_recording()

    def stop(self):
        """
        Gracefully shutdown the camera monitor.
        """
        logging.info("Shutting down the camera monitor...")
        self.should_stop = True

        # wait for the camera monitor to stop
        self.join()
