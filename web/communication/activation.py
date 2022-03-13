from urllib.parse import urljoin

from django.conf import settings
from django.template.loader import get_template

from .base import send_email

BASE_CONTEXT = {
    "token": "",
    "button_link": "",
    "recipient": None,
}


def send_account_activated_email(to, recipient):
    context = dict(BASE_CONTEXT)
    context["recipient"] = recipient
    subject = "NextMotion account activated"
    template = get_template("communication/activated_account/body.html")
    html = template.render(context=context)
    send_email(to=to, subject=subject, body_html=html)
    return html
