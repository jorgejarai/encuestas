#from __main__ import app
from operator import ge
#from flask_cors import cross_origin
#from db.users import Users

from smtplib import SMTP
from os import getenv
#from typing import List, Optional
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from db.link_sessions import LinkSessions
class Email:

    def __init__(self) -> None:
        self.server = SMTP(
            host = getenv('SMTP_HOSTNAME'),
            port = getenv('SMTP_TLS_PORT')
        )
    def connect_server(self):
        self.server.starttls()
        self.server.login(
            user = getenv('SMTP_USER'),
            password = getenv('SMTP_PASSWORD')
        )

    def send_email(self,emails:list,subject: (str),**kwargs):
        self.connect_server()
        aux = 0
        for email in emails:
            aux +=1
            mime = MIMEMultipart()
            mime['From'] = getenv('SMTP_USER')
            mime['To'] = email
            mime['Subject'] = subject
            link_path = LinkSessions().add(email,kwargs['id_encuesta'])
            link = f"http://localhost:6003/{link_path}"
            format = MIMEText(kwargs['message_format'].replace("$link_correo",link), kwargs['format'])
            mime.attach(format)
            try:
                self.server.sendmail(getenv('SMTP_USER'),email,mime.as_string())
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e)
                }
            if(aux == len(emails)):
                self.disconnect_server()


    def disconnect_server(self):
        self.server.quit()
        self.server.close()
