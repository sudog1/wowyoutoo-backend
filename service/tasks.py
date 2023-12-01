from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
import base64
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@shared_task
def send_email(email_list, data):
    context = {
        "content": data["content"],
        "image_url": "http://localhost:8000/{}".format(data["image"]),  # 배포시 도메인이름으로
    }

    html_mail = render_to_string("email.html", context)
    email = EmailMessage(
        data["title"],
        html_mail,
        to=email_list,
    )
    email.content_subtype = "html"
    email.send()
