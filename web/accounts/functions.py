from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import requests

def send_activate_email(subject, host, user, token):
    from_email = settings.DEFAULT_FROM_EMAIL
    html_content = render_to_string('accounts/activation_email.html', {
        'button_link': f"{host}/accounts/activate_account/{token}",
        'user': user, 
        }) 
    text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email,])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_simple_message(subject, host, user, token):
    html_content = render_to_string('accounts/activation_email_2.html', {
        'button_link': f"{host}/accounts/activate_account/{token}",
        'user': user, 
        }) 
    url = "https://api.eu.mailgun.net/v3/serwiswrybnej.pl/messages"
    auth = ("api", settings.MAILGUN_API_KEY )
    data = {
        "from": "no-reply@serwiswrybnej.pl",
        "to": [user.email,],
        "subject": subject,
        "html": html_content}
    data['h:Reply-To']="Michał Pielak <mpielak@okcode.eu>"
    return requests.post(url, auth=auth, data=data)