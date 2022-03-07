from web.models import Images
from uuid import uuid4


def logo(request):
    return {"logo": Images.objects.filter(logo=True).first()}


def get_domain(request):
    host = request.scheme + "://" + request.get_host()
    ctx = {
        "get_domain": host,
        "domain": request.get_host(),
        "version": "1.0",
    }
    return ctx

def get_cache_uuid(request):
    ctx = {
        "uuid": uuid4(),
        "domain": request.get_host(),
        "version": "1.0",
    }
    return ctx

def base_context_processor(request):
    # return {
    #     'BASE_URL': "http://%s" % Site.objects.get_current().domain
    # }
    # or if you don't want to use 'sites' app
    return {"BASE_URL": request.build_absolute_uri("/").rstrip("/")}
