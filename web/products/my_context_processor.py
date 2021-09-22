from web.models.products import Category


def menu_category(request):
    categorys = Category.objects.all()
    ctx = {'categorys': categorys,
            "version": "1.0",}
    return ctx

