from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls import url

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("user_register/", register_user, name="register_user"),
    path("activate_account/<token>", activate_account, name="activate_account"),
    path(
        "company_registration/",
        company_registration,
        name="company_registration",
    ),
    path("konto_uzytkownika", user_account, name="user_account"),
    path("pofil_uzytkownika", user_profile, name="user_profile"),
    path("zamowienia", user_orders, name="user_orders"),
    path("zmiana_hasla", change_password, name="change_password"),
    path("adresy_uzytkownika", user_addresses, name="user_address"),
    #      name='register_user_basket'),
    #      AddClientFromBasketView.as_view(),
    #      name='register_user_basket'),
    # path('wybor_konta/',
    #      ChoiceAccountReqisterView.as_view(),
    #      name='choice_register'),
    # path('rejestracja_klienta_koszyk/',
    #      AddClientFromBasketView.as_view(),
    #      name='register_user_basket'),
    # path('rejestracja_klienta_biznesowego_koszyk/',
    #      AddBusinessClientFromBasketView.as_view(),
    #      name='register_bisness_user_basket'),
    # path('dodaj_adres_koszyk/',
    #      AddAddressBasketView.as_view(),
    #      name='add_address_basket'),
    # path('edytuj_adres_koszyk/<int:pk>/',
    #      UpdateAddressBasketView.as_view(),
    #      name='edit_address_basket'),
    # path('usun_adres_koszyk/<int:pk>/',
    #      DeleteAddressBasketView.as_view(),
    #      name='delete_address_basket'),
    # path('password_change/',
    #      auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password_change/done/',
    #      auth_views.PasswordChangeDoneView.as_view(),
    #      name='password_change_done'),
    # path('password_reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path('password_reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('reset/done/',
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),
    #     path('change_user_password/<int:pk>',
    #          ChangeOnlyPasswordView.as_view(),
    #          name='change_only_password'),
]
