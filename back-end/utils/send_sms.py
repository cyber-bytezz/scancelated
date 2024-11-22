import os
from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv(override=True)

# Twilio credentials
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
from_phone_number = os.getenv('FROM_PHONE_NUMBER')
#to_phone_number = os.getenv('TO_PHONE_NUMBER')


# Initialize Twilio client
client = Client(account_sid, auth_token)

# Message to be sent
#message_body = "Your DICOM files have been pushed to viatronix successfully."


def send_sms(message_body,to_phone_number):
    try:
        # Send SMS using Twilio
        message = client.messages.create(body=message_body, from_=from_phone_number, to=to_phone_number)
        print(f"SMS sent successfully. SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS. Error: {e}")


#send_sms()
