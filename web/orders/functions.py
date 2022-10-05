import os
import json
from datetime import datetime

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from web.models import ActivateToken, Invoices, Orders


def new_number(store_id, year, month, day):
    try:
        last_number = Orders.objects.filter(store_id=store_id).first()
        if last_number:
            number_indx = int(last_number.number[:3]) + 1
            ln_day = last_number.created_time.day
            if ln_day != day:
                number_indx = 1
            if number_indx < 10:
                if day > 9:
                    number_format = f"00{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"00{number_indx}/0{day}/{month}/{year}"
            if 100 > number_indx > 9:
                if day > 9:
                    number_format = f"0{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"0{number_indx}/0{day}/{month}/{year}"
            if 999 > number_indx > 99:
                if day > 9:
                    number_format = f"{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"{number_indx}/0{day}/{month}/{year}"
            if number_indx > 999:
                if day > 9:
                    number_format = f"{number_indx}/{day}/{month}/{year}"
                else:
                    number_format = f"{number_indx}/0{day}/{month}/{year}"
        else:
            number_format = f"001/{day}/{month}/{year}"
        return number_format
    except Orders.DoesNotExist:
        number_format = f"001/{day}/{month}/{year}"
        return number_format


def new_invoice_number():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    try:
        last_number = Invoices.objects.all().first()
        if last_number:
            last_number.number = last_number.number.replace("pdf/faktura_", "").replace(
                ".pdf", ""
            )
            number_indx = int(last_number.number[:3]) + 1
            ln_month = last_number.created_time.month
            ln_year = last_number.created_time.year
            if ln_month != month or ln_year != year:
                number_indx = 1
            if number_indx < 10:
                if day > 9:
                    number_format = f"00{number_indx}-{day}-{month}-{year}"
                else:
                    number_format = f"00{number_indx}-0{day}-{month}-{year}"
            if 100 > number_indx > 9:
                if day > 9:
                    number_format = f"0{number_indx}-{day}-{month}-{year}"
                else:
                    number_format = f"0{number_indx}-0{day}-{month}-{year}"
            if 999 > number_indx > 99:
                if day > 9:
                    number_format = f"{number_indx}-{day}-{month}-{year}"
                else:
                    number_format = f"{number_indx}-0{day}-{month}-{year}"
            if number_indx > 999:
                if day > 9:
                    number_format = f"{number_indx}-{day}-{month}-{year}"
                else:
                    number_format = f"{number_indx}-0{day}-{month}-{year}"
            number_format += "-WWW"
        else:
            number_format = f"001-{day}-{month}-{year}-WWW"
        return number_format
    except Invoices.DoesNotExist:
        number_format = f"001-{day}-{month}-{year}-WWW"
        return number_format


def create_invoice(order):
    invoice_number = new_invoice_number()
    file_name = "pdf/faktura-" + invoice_number + ".pdf"
    invoice, created = Invoices.objects.get_or_create(pdf=file_name, order=order)
    invoice.order = order
    invoice.number = invoice_number
    invoice.save()
    return invoice, created, file_name


def create_pdf_invoice(order):
    invoice, created, file_name = create_invoice(order)
    if not created:
        os.remove(os.path.join(settings.MEDIA_ROOT + file_name))
    order.invoice = invoice
    order.save()
    context = {"order": order, "invoice": order.invoice}
    html_string = render_to_string("orders/invoice.html", context)

    html = HTML(string=html_string)
    html.write_pdf(target=settings.MEDIA_ROOT + str(invoice.pdf))
    return file_name


def order_inpost_box(request, order, delivery_method):
    if order.pay_method.pay_method == 4 and order.delivery_method.inpost_box:
        try:
            order.inpost_box = request.session["inpost_box_id"]
            order.products_item.get("dm" + str(delivery_method.id))
            if not order.products_item.get("dm" + str(delivery_method.id)):
                order.products_item.update(delivery_method.delivery_dict)
            del request.session["inpost_box_id"]
        except KeyError:
            pass


def send_email_order_completed(order, host, file_name=False):
    token = ActivateToken.objects.get(user=order.client).activation_token
    html_content = render_to_string(
        "orders/order_completed_email.html",
        {
            "order": order,
            "user": order.client.profile,
            "button_link": f"{host}/zamowienia/redirect_from_email/{token}",
        },
    )
    url = "https://api.eu.mailgun.net/v3/serwiswrybnej.pl/messages"
    auth = ("api", settings.MAILGUN_API_KEY)

    subject = "Zamówienie nr: " + order.number
    data = {
        "from": "no-reply@serwiswrybnej.pl",
        "to": [order.client.email, "michal.pielak81@gmail.com"],
        "subject": subject,
        "html": html_content,
    }
    data["h:Reply-To"] = "Michał Pielak <michal.pielak81@gmail.com>"
    if file_name:
        invoice_file_path = os.path.join(settings.MEDIA_ROOT + file_name)
        files = [
            (
                "attachment",
                (
                    "faktura-" + order.invoice.number + ".pdf",
                    open(invoice_file_path, "rb").read(),
                ),
            ),
        ]
        return requests.post(url, auth=auth, data=data, files=files)
    return requests.post(url, auth=auth, data=data)


def send_email_order_completed_by_django(order, host, file_name=False):
    subject, from_email, to = (
        f"Zamówienie w serwisie w Rybnej nr: {order.number} zakończono pomyślnie.",
        settings.EMAIL_HOST_USER,
        [order.client.email,]
    )
    token = ActivateToken.objects.get(user=order.client).activation_token
    html_content = render_to_string(
        "orders/order_completed_email.html",
        {
            "order": order,
            "user": order.client.profile,
            "button_link": f"{host}/zamowienia/redirect_from_email/{token}",
        },
    )
    html_content = html_content
    msg = EmailMultiAlternatives(subject, html_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    if file_name:
        msg.attach("faktura-" + order.invoice.number + ".pdf", order.invoice.pdf.read())
    msg.send()

def send_email_order_owner_completed_by_django(order, host, file_name=False):
    subject, from_email, to = (
        f"Zamówienie w serwisie w Rybnej nr: {order.number} zakończono pomyślnie.",
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_USER]
    )
    token = ActivateToken.objects.get(user=order.client).activation_token
    html_content = render_to_string(
        "orders/order_completed_email.html",
        {
            "order": order,
        },
    )
    html_content = render_to_string(
        "orders/order_completed_email_for_owner.html",
        {
            "order": order,
            "products": order.products_item,
        },
    )
    html_content = html_content
    msg = EmailMultiAlternatives(subject, html_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    if file_name:
        msg.attach("faktura-" + order.invoice.number + ".pdf", order.invoice.pdf.read(), 'application/pdf')
    msg.send()
