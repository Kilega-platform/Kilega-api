import smtplib
from config.db_connection import app_configuration
from dotenv import load_dotenv
from email.message import EmailMessage
from email.utils import make_msgid
load_dotenv()

MAIL_USERNAME = app_configuration.MAIL_USERNAME
MAIL_PASSWORD = app_configuration.MAIL_PASSWORD
MAIL_SERVER = app_configuration.MAIL_SERVER
MAIL_PORT = app_configuration.MAIL_PORT


def send_email(subject, sender, recipients, body):
    msg = EmailMessage()
    msg['Message-ID'] = make_msgid()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)

    with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT) as smtp:
        smtp.login(MAIL_USERNAME, MAIL_PASSWORD)

        smtp.send_message(msg)
