import requests
from django.conf import settings
from django.template.loader import render_to_string


def send_simple_message(subject, host, user, token):
    html_content = render_to_string(
        "accounts/activation_email.html",
        {
            "button_link": f"{host}/accounts/activate_account/{token}",
            "user": user,
        },
    )
    url = "https://api.eu.mailgun.net/v3/serwiswrybnej.pl/messages"
    auth = ("api", settings.MAILGUN_API_KEY)
    data = {
        "from": "no-reply@serwiswrybnej.pl",
        "to": [
            user.email,
        ],
        "subject": subject,
        "html": html_content,
    }
    data["h:Reply-To"] = "Michał Pielak <pielak@miktelgsm.pl>"
    return requests.post(url, auth=auth, data=data)

def send_activate_info_message(user):
    subject = f"Nowy użytkownik w serwisie {user.email}"
    html_content = render_to_string(
        "accounts/activation_info_email.html",
        {
            "user": user,
        },
    )
    url = "https://api.eu.mailgun.net/v3/serwiswrybnej.pl/messages"
    auth = ("api", settings.MAILGUN_API_KEY)
    data = {
        "from": "no-reply@serwiswrybnej.pl",
        "to": [
            "pielak@miktelgsm.pl",
        ],
        "subject": subject,
        "html": html_content,
    }
    data["h:Reply-To"] = "Michał Pielak <pielak@miktelgsm.pl>"
    return requests.post(url, auth=auth, data=data)