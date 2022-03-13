import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_contact_message(subject, message):
    url = "https://api.eu.mailgun.net/v3/serwiswrybnej.pl/messages"
    auth = ("api", settings.MAILGUN_API_KEY)
    data = {
        "from": "no-reply@serwiswrybnej.pl",
        "to": f"Klient <{ settings.DEFAULT_FROM_EMAIL }>",
        "subject": subject,
        "text": message,
    }
    return requests.post(url, auth=auth, data=data)


def send_email_contact_message_by_django(subject, message):
    html_content = message
    msg = EmailMultiAlternatives(
        subject, html_content, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
