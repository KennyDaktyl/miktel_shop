from web.models.products import Category


def menu_category(request):
    categorys = Category.objects.all()
    ctx = {'categorys': categorys,
            "version": "1.0",}
    return ctx

def get_domain(request):
    host = request.scheme + "://" + request.get_host()
    ctx = {'get_domain': host,
            "version": "1.0",}
    return ctx

