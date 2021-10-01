from web.models import Images


def logo(request):
    return {'logo': Images.objects.filter(logo=True).first()}
