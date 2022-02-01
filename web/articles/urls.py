from django.urls import path
from . import views


urlpatterns = [
    path("artykuly/<slug:category>/<slug:title>/<int:pk>",
         views.article_details, name='article_details'),
    path("artykuly", views.articles_list, name='articles_list'),
]
