from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls import url

urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("user_register/", register_user, name="register_user"),
    path(
        "activate_account/<token>", activate_account, name="activate_account"
    ),
    path(
        "company_registration/",
        company_registration,
        name="company_registration",
    ),
    path("konto_uzytkownika", user_account, name="user_account"),
    path("profil_uzytkownika", user_profile, name="user_profile"),
    path("zamowienia", user_orders, name="user_orders"),
    path("zmiana_hasla", change_password, name="change_password"),
    path("adresy_uzytkownika", user_addresses, name="user_address"),
]
