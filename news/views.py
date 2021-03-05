# from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView  # импортируем класс, который говорит нам о том, что в этом
# представлении мы будем выводить список объектов из БД
from .models import Post
from datetime import datetime
from .filters import NewsFilter


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-article_time_in']
    paginate_by = 1  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого
        # фильтра
        context['test'] = ''
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
