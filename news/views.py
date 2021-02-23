# from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView  # импортируем класс, который говорит нам о том, что в этом
# представлении мы будем выводить список объектов из БД
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
