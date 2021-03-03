# from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView  # импортируем класс, который говорит нам о том, что в этом
# представлении мы будем выводить список объектов из БД
from .models import Post
from datetime import datetime


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-article_time_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого
        # фильтра
        context['test'] = ''
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
