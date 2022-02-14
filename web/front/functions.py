import requests
from django.conf import settings
from django.template.loader import render_to_string


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
