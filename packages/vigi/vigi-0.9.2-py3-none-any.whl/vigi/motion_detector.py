"""
This module contains the MotionDetector class that is used to detect motion in a video stream.
"""

import cv2
import numpy as np

from vigi.utils.spatial import boxes_intersect
from vigi.utils.drawing import draw_bboxes, draw_bbox, draw_title

class MotionDetector():
    """
    The MotionDetector class is used to detect motion in a video stream.
    """
    def __init__(self, object_detection_model=None, inference_device=None,
                 debug=False, sensitivity=0.5):
        """
        Initialize the motion detector with the given sensitivity and motion callback.
        The motion callback is called when motion is detected.
        sensitivity: float, the sensitivity of the motion detector, should be between 0 and 1
        """
        self.sensitivity = sensitivity
        self.back_sub = cv2.createBackgroundSubtractorMOG2(
            # the higher the sensitivity, the lower the threshold
            varThreshold=(50 / self.sensitivity),
            detectShadows=True
        )
        self.motion_callback = None
        self.motion_detected = False
        self.debug = debug
        self.skip_frames_count = 50 # warming up frames count
        self.object_detection_model = object_detection_model
        self.inference_device = inference_device
        self.reset_motion_flag_after = 0

    def set_motion_callback(self, motion_callback):
        """
        Set the motion callback that will be called when motion is detected.
        """
        self.motion_callback = motion_callback

    def is_motion_detected(self) -> bool:
        """
        Returns True if motion is being detected, otherwise False.
        """
        return self.motion_detected

    def update(self, frame):
        """
        Update the motion detector with the current frame and return the
        frame with the motion detection overlay.
        """
        original_frame = frame.copy()

        # convert the current frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # update the background model to get the foreground mask
        fg_mask = self.back_sub.apply(gray_frame)

        # Warming up the model by skipping the first few frames
        if self.skip_frames_count > 0:
            self.skip_frames_count -= 1

            draw_title(original_frame, 'WARMING UP')
            return (original_frame, set())

        # threshold the mask, the min_thresh value is set to 100 by default
        # this value roughly impacts the sensitivity of the motion detection
        min_thresh = 50 / self.sensitivity # the higher the sensitivity, the lower the threshold
        _, motion_mask = cv2.threshold(fg_mask, thresh = min_thresh,
                                       maxval = 255, type = cv2.THRESH_BINARY)

        # median blur to remove granular noise
        motion_mask = cv2.medianBlur(motion_mask, ksize = 3)

        # morphological operations to fill in holes
        kernel = np.array((15,15), dtype=np.uint8)

        # morphologyEx with MORPH_OPEN is the same as erode followed by dilate
        motion_mask = cv2.morphologyEx(motion_mask, op = cv2.MORPH_OPEN,
                                       kernel = kernel, iterations = 1)

        # morphologyEx with MORPH_CLOSE is the same as dilate followed by erode
        motion_mask = cv2.morphologyEx(motion_mask, op = cv2.MORPH_CLOSE,
                                       kernel = kernel, iterations = 1)

        # get contours of the moving objects in the frame
        contours, _ = cv2.findContours(motion_mask, mode = cv2.RETR_EXTERNAL,
                                       method = cv2.CHAIN_APPROX_SIMPLE)
        detections = []

        # the higher the sensitivity, the lower the are threshold
        cnt_area_thresh = 2500 / self.sensitivity
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > cnt_area_thresh:
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, x + w, y + h])

        detections = np.array(detections)

        if len(detections) > 0:
            # Motion detected!
            if self.motion_detected is False:
                self.motion_detected = True
                if self.motion_callback:
                    self.motion_callback()

            self.reset_motion_flag_after = 2 # frames

            if self.debug:
                draw_bboxes(original_frame, detections)
        else:
            if self.motion_detected:
                if self.reset_motion_flag_after > 0:
                    self.reset_motion_flag_after -= 1
                else:
                    self.motion_detected = False

        if self.motion_detected:
            # draw red rectangle on frame
            cv2.rectangle(original_frame, (0, 0),
                          (original_frame.shape[1], original_frame.shape[0]),
                          (0, 0, 255), 10)
            # draw text on frame
            cv2.putText(original_frame, 'MOTION DETECTED', (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        detected_objects = set()
        if self.motion_detected:
            if self.object_detection_model:
                results = self.object_detection_model(original_frame,
                                                      device = self.inference_device,
                                                      verbose = self.debug)

                for result in results:
                    # move to cpu
                    result = result.cpu()

                    for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                        label = result.names[int(cls)]
                        detected_objects.update([label])
                        display = False

                        # check if this box intersects with any of the detections
                        for detection in detections:
                            if boxes_intersect(box, detection):
                                display = True

                        if display:
                            draw_bbox(original_frame, box, label=label)

        return (original_frame, detected_objects)
