from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


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

