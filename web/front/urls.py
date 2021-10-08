from django.urls import path
from . import views


urlpatterns = [
    path("", views.first_page, name='front_page'),
    path("kontakt", views.contact_page, name='contact_page'),
    path("polityka-prywatnosci", views.privacy_policy, name='privacy_policy'),
    path("regulamin", views.terms_rules, name='terms')
]
