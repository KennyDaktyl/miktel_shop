from django import template
import datetime

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()

<<<<<<< HEAD

@register.filter
def plus_days(value, days):
    return (value + datetime.timedelta(days=days)).date()
=======
@register.filter
def plus_days(value, days):
    return (value + datetime.timedelta(days=days)).date()
>>>>>>> 561ed0dae4ae1a36bc77768a2520cb44e3b3c9de
