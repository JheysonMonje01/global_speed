from flask_mail import Message, Mail
from flask import current_app

mail = Mail()

class EmailSender:
    @staticmethod
    def send_email(to_email, subject, body):
        msg = Message(subject, recipients=[to_email], body=body)
        mail.send(msg)
