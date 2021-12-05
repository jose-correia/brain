from typing import List
from flask import current_app

class SendMailService():
    def __init__(self, recipients, subject, content=""):
        self.subject = subject
        self.content = content
        self.recipients = recipients

    def call(self):
        try:
            current_app.mail.send_message(subject=self.subject, recipients=self.recipients, html=self.content)
            return True
        except:
            return False