from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Article, Category
from django.views.generic import ListView, DetailView


class ArticleList(ListView):
    # model = Article
    # context_object_name = 'articles' # This item Default is object_list
    #     context = {
    #         "articles": articles # It Changed to Somting like "object_list" : page_obj
    #     }
    #template_name = 'blog/article_list.html' # default article_list
    queryset = Article.objects.published()
    paginate_by = 2



class ArticleDetail(DetailView):

    #template_name = 'blog/article_detail.html' # Default is article_detail.html

    def get_object(self):
        slug = self.kwargs.get('slug')   # keyword Arguments
        return get_object_or_404(Article, slug=slug, status='p')


class CategoryList(ListView):
    paginate_by = 2
    #template_name = 'blog/list.html'  # default article_list

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')  # keyword Arguments
        category = get_object_or_404(Category.objects.active(), slug=slug )
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category']= category
        return context


class AuthorList(ListView):
    paginate_by = 2
    #template_name = 'blog/list.html'  # default article_list

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')  # keyword Arguments
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


# def detail(request, slug):
#     context = {
#         'article': get_object_or_404(Article, slug=slug, status='p')
#     }
#     return render(request, 'blog/article_detail.html', context)


# def home(request, page=1):
#     article_list = Article.objects.published()
#     paginator = Paginator(article_list, 2)  # Show 5 article per page.
#     articles = paginator.get_page(page)
#     context = {
#         "articles": articles
#     }
#     return render(request, 'blog/article_list.html', context)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     article_list = category.articles.published()
#     paginator = Paginator(article_list, 2)  # Show 5 article per page.
#     articles = paginator.get_page(page)
#     context = {
#
#         'articles': articles,
#         'category': category
#     }
#     return render(request, 'blog/list.html', context)
#
