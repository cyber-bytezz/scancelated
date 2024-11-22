# load env

from dotenv import load_dotenv
load_dotenv(override=True)

import smtplib
import  os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.exceptions import HTTPException

msg = EmailMessage()

HOST = os.getenv('SMTP_HOST')
PORT = os.getenv('SMTP_PORT')
FROM_EMAIL = os.getenv('FROM_EMAIL')
PASSWORD = os.getenv('PASSWORD')

smtp = smtplib.SMTP(HOST, PORT)

import requests
from email.mime.image import MIMEImage
from fastapi import HTTPException

def send_email(to_email_id, subject, content_to_be_sent):
    try:
        smtp = smtplib.SMTP(HOST, PORT)
        smtp.starttls()
        smtp.login(FROM_EMAIL, PASSWORD)
        
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email_id

        # Create the body with HTML content
        msg_alt = MIMEMultipart('alternative')
        msg.attach(msg_alt)

        # Attach the HTML content
        html_content = MIMEText(content_to_be_sent, 'html')
        msg_alt.attach(html_content)

        # Fetch the image from the URL
        logo_url = "https://devb1fb.blob.core.windows.net/colowatch-assets/colowatchlogo.png"
        response = requests.get(logo_url)
        response.raise_for_status()  # Check for HTTP errors
        img = MIMEImage(response.content)
        img.add_header('Content-ID', '<logo>')
        img.add_header('Content-Disposition', 'inline', filename='colowatchlogo.png')
        msg.attach(img)

        smtp.sendmail(FROM_EMAIL, to_email_id, msg.as_string())
        smtp.quit()
        return {"message": "Mail sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Not able to send email: {str(e)}')
