import random
from django.core.mail import EmailMessage, send_mail
import os
from django.conf import settings
# def send_mails(data):
#     res = send_mail(data.get("subject"),
#               data.get("message"),
#             fail_silently=False,recipient_list=[[data["to_email"]]],from_email=settings.DEFAULT_FROM_EMAIL)
#     print(res)
def send_mails(data):
    email = EmailMessage(subject=data['subject'], body=data['body'], to=[data['to_email']])

    email.send()
def generate_otp():
          return str(random.randint(100000, 999999)) 