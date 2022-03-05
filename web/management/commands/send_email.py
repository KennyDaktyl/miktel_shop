from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class Command(BaseCommand):
    def handle(self, *args, **options):
        html_content = render_to_string(
        "orders/order_completed_email.html",
        {
        },
    )
        url = "https://api.eu.mailgun.net/v3/serwiswrybnej.pl/messages"
        auth = ("api", settings.MAILGUN_API_KEY)

        subject = "Zamówienie nr: TEST"
        data = {
        "from": "admin@serwiswrybnej.pl",
        "to": ["pielak@miktelgsm.pl"],
        "subject": subject,
        "html": html_content,
        }
        data["h:Reply-To"] = "Michał Pielak <pielak@miktelgsm.pl>"
        requests.post(url, auth=auth, data=data)

        
