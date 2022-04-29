from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect
from web.models.articles import Articles
from web.models.products import Category


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
    
    def get_queryset(self):
        articles = Articles.objects.all()
        if self.request.GET.get('typ'):
            self.category = get_object_or_404(
            Category, pk=self.request.GET.get('typ')
            )
            return articles.filter(category=int(self.request.GET.get('typ')))
        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_pk = self.object_list.values_list(
            'category', flat=True).distinct().order_by()
        context["categories"] = Articles.objects.filter(pk__in=[categories_pk])
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
