from re import template
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

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

article_details = ArticleDetails.as_view()
articles_list = ArticleList.as_view()
