from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect
from web.models.articles import Articles


class ArticleDetails(DetailView):
    model = Articles
    template_name = "articles/article_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArticleList(ListView):
    model = Articles
    paginate_by = 30
    template_name = "articles/articles_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArticlesListRedirectView(RedirectView):
    permanent = False
    pattern_name = "articles_list"


class ArticleRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get(self, *args, **kwargs):
        article = get_object_or_404(
            Articles, pk=kwargs["pk"])
        return redirect(article.get_absolute_url())

article_details = ArticleDetails.as_view()
articles_list = ArticleList.as_view()
redirect_articles_list = ArticlesListRedirectView.as_view()
redirect_article = ArticleRedirectView.as_view()
