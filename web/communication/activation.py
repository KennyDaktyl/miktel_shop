from urllib.parse import urljoin

from django.conf import settings
from django.template.loader import get_template

from .base import send_email

# from web.communication.system.commons import BASE_CONTEXT


# # STAFF -> collaborator, assistant, next doctor, etc.


# def get_clinic_activation_url(token, ios):
#     return urljoin(settings.WEB_UI_BASE_URL, f"/auth/signup/activate?token={token}&ios={ios}")


# def get_staff_activation_url(token):
#     return urljoin(settings.WEB_UI_BASE_URL, f"/auth/activate-simple?token={token}")


# # Probably will not be used anymore. Template configured per clinic in communication settings.
# # def get_patient_activation_url(token):
# #     return get_staff_activation_url(token)


# def get_clinic_activation_template(token, recipient):
#     context = dict(BASE_CONTEXT)
#     context["recipient"] = recipient
#     context["token"] = token
#     ios = not recipient.web_registration
#     context["button_link"] = get_clinic_activation_url(token, str(ios).lower())
#     template = get_template("communication/activation_account_clinic/nm.min.html")
#     return template.render(context=context)


# def get_staff_activation_template(token, recipient):
#     context = dict(BASE_CONTEXT)
#     context["recipient"] = recipient
#     context["button_link"] = get_staff_activation_url(token)
#     template = get_template("communication/activation_account_staff/body.html")
#     return template.render(context=context)


# def send_activation_email(to, html):
#     subject = "NextMotion account activation"
#     return send_email(to=to, subject=subject, body_html=html)


# def send_clinic_activation_email(to, token, recipient):
#     html = get_clinic_activation_template(token, recipient)
#     send_activation_email(to, html)
#     return html


# def send_staff_activation_email(to, token, recipient):
#     html = get_staff_activation_template(token, recipient)
#     send_activation_email(to, html)
#     return html


# # Probably will not be used anymore. Template configured per clinic in communication settings.
# # def send_patient_activation_email(to, token, recipient, doctor):
# #     html = get_patient_activation_template(token, recipient, doctor)
# #     send_activation_email(to, html)
# #     return html

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
