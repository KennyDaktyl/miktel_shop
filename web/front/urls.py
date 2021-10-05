from django.urls import path
from . import views


urlpatterns = [
    path("", views.first_page, name='front_page'),
    path("kontakt", views.contact_page, name='contact_page'),
]
