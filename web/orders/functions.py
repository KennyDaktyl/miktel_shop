from django.core.files import File
from django.conf import settings
import os
from web.models import Invoices
from io import StringIO
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
import stripe
from django.contrib import messages

from web.models import Orders


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


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(
        src=BytesIO(html.encode('UTF-8')),
        dest=result,
        encoding='UTF-8'
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def create_pdf_invoice(order):
    invoice_number = (order.number).replace("/", "-")
    filename = f"faktura_{invoice_number}_WWW.pdf"
    invoice, created = Invoices.objects.get_or_create(
        pdf=filename)
    print(created)
    if not created:
        os.remove(os.path.join(
            settings.MEDIA_ROOT + "pdf/" + str(invoice.pdf)))
    order.pdf = invoice
    order.save()
    invoice.number = f"{invoice_number}_WWW"
    pdf = render_to_pdf('orders/invoice.html',
                        {'order': order, 'invoice': invoice})
    invoice.pdf.save(filename, File(BytesIO(pdf.content)))
