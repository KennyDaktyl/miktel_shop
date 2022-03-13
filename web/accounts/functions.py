import requests
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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
        "from": "rejestracja@serwiswrybnej.pl",
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
        "from": "admin@serwiswrybnej.pl",
        "to": [
            "pielak@miktelgsm.pl",
        ],
        "subject": subject,
        "html": html_content,
    }
    data["h:Reply-To"] = "Michał Pielak <pielak@miktelgsm.pl>"
    return requests.post(url, auth=auth, data=data)


def send_activate_email_by_django(subject, host, user, token):
    subject, from_email, to = subject, settings.EMAIL_HOST_USER, user.email
    html_content = render_to_string(
        "accounts/activation_email.html",
        {
            "button_link": f"{host}/accounts/activate_account/{token}",
            "user": user,
        },
    )
    html_content = html_content
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_activate_info_email_by_django(user):
    subject, from_email, to = (
        f"Nowy użytkownik w serwisie {user.email}",
        settings.EMAIL_HOST_USER,
        settings.EMAIL_HOST_USER,
    )
    html_content = render_to_string(
        "accounts/activation_info_email.html",
        {
            "user": user,
        },
    )
    html_content = html_content
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
