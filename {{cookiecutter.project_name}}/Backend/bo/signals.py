# *coding: utf-8*
import logging,os
from django.core.files.storage import default_storage
from django.db.models import FileField
from django.core.mail import send_mail
import sendgrid
from PIL import Image
import googlemaps
from django.db.models.signals import pre_delete,post_save,post_delete,pre_save
from {{cookiecutter.project_name}} import settings
logger = logging.getLogger('django')



def envoiMessageMailGenerique(TEMPLATE_ID,email,message):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": email
                    }
                ],
                "dynamic_template_data": {
                    "pseudo": message
                }
            }
        ],
        "from": {
            "email": "flip! <jab12121@live.com>"
        },
        "dynamic_template_data": {
            "pseudo":message
        },
        "template_id": TEMPLATE_ID
    }
    logger.info("[SMTP] on envoi data %s"%data)
    response = sg.client.mail.send.post(request_body=data)
    logger.info("[SMTP] reponse %s"%response)
    return response

def envoiMessageMail(email,subject,message):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": email
                    }
                ],
                "dynamic_template_data": {
                    "message":message,
                    "subject":subject
                }
            }
        ],
        "from": {
            "email": "flip! <jab12121@live.com>"
        },
        "template_id": settings.MESSAGE_TEMPLATE_ID
    }
    logger.info("[SMTP] on envoi data %s" % data)
    response = sg.client.mail.send.post(request_body=data)
    logger.info("[SMTP] reponse %s" % response)
    return


def sendEmailError(e):
    email = "csurbier@idevotion.fr"
    subject = "Backend {{cookiecutter.project_name}}: Exception"
    message = "Message:%s"%e
    envoiMessageMail(email, message, subject)

def sendEmailBasique(subject,message):
   email = "csurbier@idevotion.fr"
   envoiMessageMail(email, subject,message)
