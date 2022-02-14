import uuid

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_email(
    subject="",
    body="",
    body_html="",
    from_email=None,
    to=None,
    cc=None,  # TODO: bcc?
    reply_to=None,
    attachments=None,
):
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    if to is not None and not isinstance(to, (list, tuple)):
        to = [to]
    if cc is not None and not isinstance(cc, (list, tuple)):
        cc = [cc]
    if reply_to is not None and not isinstance(reply_to, (list, tuple)):
        reply_to = [reply_to]
    if attachments is not None and not isinstance(attachments, (list, tuple)):
        attachments = [attachments]

    msg_id = str(uuid.uuid4())
    headers = {
        "Message-ID": msg_id
    }  # TODO: check in Sendgrid if emails can be tracked somehow, delivery status etc.
    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
        cc=cc,
        reply_to=reply_to,
        attachments=attachments,
        headers=headers,
    )
    if body_html:
        msg.attach_alternative(body_html, "text/html")
    try:
        msg.send()
    except Exception:
        return False
    return True
