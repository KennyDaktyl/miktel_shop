import os
import requests
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from weasyprint import HTML

from web.models import Invoices, Orders, ActivateToken


def new_number(store_id, year, month, day):
    try:
        last_number = Orders.objects.filter(store_id=store_id).first()
        if last_number:
            number_indx = int(last_number.number[:3]) + 1
            ln_day = last_number.date.day
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

from datetime import datetime

def new_invoice_number():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    try:
        last_number = Invoices.objects.all().first()
        if last_number:
            last_number.number = last_number.number.replace("pdf/faktura_", "").replace(".pdf", "")
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



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(
        src=BytesIO(html.encode("UTF-8")), dest=result, encoding="UTF-8"
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def create_pdf_invoice(order, invoice, created, file_name):
    if not created:
        os.remove(
            os.path.join(settings.MEDIA_ROOT + file_name)
        )
    order.invoice_created = invoice
    order.save()
    context = {
        "order": order, "invoice": order.invoice_created
    }
    html_string = render_to_string("orders/invoice.html", context)

    html = HTML(string=html_string)
    html.write_pdf(target=settings.MEDIA_ROOT + str(invoice.pdf))


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
        "to": [
            order.client.email, "pielak@miktelgsm.pl"
        ],
        "subject": subject,
        "html": html_content,
    }
    data["h:Reply-To"] = "Michał Pielak <pielak@miktelgsm.pl>"
    if file_name:
        invoice_file_path = os.path.join(settings.MEDIA_ROOT + file_name)
        files=[("attachment", ("Faktura " + order.invoice_created.number, open(invoice_file_path, "rb").read())),]
        return requests.post(url, auth=auth, data=data, files=files)
    return requests.post(url, auth=auth, data=data)
    