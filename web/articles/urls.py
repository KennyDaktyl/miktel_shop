from django.urls import path
from .views import article_details, articles_list, \
    redirect_article, redirect_articles_list


urlpatterns = [
    path(
        "<slug:category>/<slug:title>/<int:pk>",
        article_details,
        name="article_details",
    ),
    path("", articles_list, name="articles_list"),
    path(
        "artykuly",
        redirect_articles_list,
        name="redirect_articles_list",
    ),
    path(
        "artykuly/<slug:category>/<slug:title>/<int:pk>",
        redirect_article,
        name="redirect_article",
    ),
]
