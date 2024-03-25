"""
This file contains the SMSNotificationProvider class, which is
responsible for sending SMS notifications.
"""
import logging

from twilio.rest import Client

class SMSNotificationProvider:
    """
    The SMSNotificationProvider class is responsible for sending SMS notifications.
    """
    def __init__(self, account_sid: str, auth_token: str, from_number: str,
                 recipient_phone_numbers: list):
        """
        :param account_sid: Twilio account SID
        :param auth_token: Twilio auth token
        :param from_number: Twilio phone number
        :param recipient_phone_numbers: List of phone numbers of the recipients
        """
        self.from_number = from_number
        self.recipient_phone_numbers = recipient_phone_numbers
        self.client = Client(account_sid, auth_token)
        logging.info("SMS notification provider initialized successfully.")

    def notify(self, notification_text):
        """
        Send SMS notification to the recipients
        """
        for recipient_phone_number in self.recipient_phone_numbers:
            self._send_sms(notification_text, recipient_phone_number)

    def _send_sms(self, notification_text, recipient_phone_number):
        """
        Send SMS to a single recipient
        """
        logging.info("Sending SMS from %s to %s with text: %s",
                     self.from_number, recipient_phone_number, notification_text)
        self.client.messages.create(
            body = notification_text,
            from_ = self.from_number,
            to = recipient_phone_number
        )
