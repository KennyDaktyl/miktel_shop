from web.models import Images


def logo(request):
    return {'logo': Images.objects.filter(logo=True).first()}


def get_domain(request):
    host = request.scheme + "://" + request.get_host()
    ctx = {
        'get_domain': host,
        'domain': request.get_host(),
        "version": "1.0",
    }
    return ctx
