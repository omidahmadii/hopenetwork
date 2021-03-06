from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from blog.models import Article

@login_required
def home(request):
    return render(request, 'registrations/home.html')


class ArticleList(LoginRequiredMixin, ListView):
    queryset = Article.objects.all()
    template_name = "reqistration/home.html"
