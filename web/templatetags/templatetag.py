from operator import le
from django import template
import datetime

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.filter
def plus_days(value, days):
    return (value + datetime.timedelta(days=days)).date()

@register.filter
def replace_decimal_point(value):
    value = str(value)
    return value.replace(",",".")


@register.filter
def plus_value(value, number):
    return value + number


@register.filter
def polish_letter(letter):
    polish = {
        "A_": "Ą",
        "E_": "Ę",
        "C_": "Ć",
        "O_": "Ó",
        "S_": "Ś",
        "Z_": "Ź",
        "Z__": "Ż"
    }
    if polish.get(letter):
        return polish.get(letter)
    return letter
