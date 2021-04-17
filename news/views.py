from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Post, Category
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.cache import cache


@login_required
def subscribe_view(request):
    category = get_object_or_404(Category, id=request.POST.get('category_id'))
    if category.category_subscriber.filter(id=request.user.id).exists():
        category.category_subscriber.remove(request.user)
        sub_trigger = False
    else:
        category.category_subscriber.add(request.user)
        sub_trigger = True
    html_context_category = {'sub_category_name': category, 'sub_category_user': request.user}
    if sub_trigger:
        html_content = render_to_string('mail_notification_subscribe.html', html_context_category)
        msg = EmailMultiAlternatives(
            subject=f'Подтверждение подписки на обновления в категории {html_context_category["sub_category_name"]} '
                    f'(velosiped.test)',
            # from_email='testun_test@mail.ru', # заменили на дефолтный в настройках
            to=['testersaitin@yandex.ru'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
    else:
        html_content = render_to_string('mail_notification_unsubscribe.html', html_context_category)
        msg = EmailMultiAlternatives(
            subject=f'Подтверждение отписки от обновлений в категории {html_context_category["sub_category_name"]} '
                    f'(velosiped.test)',
            from_email='testun_test@mail.ru',
            to=['testersaitin@yandex.ru'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
    return redirect('index')


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-article_time_in']
    paginate_by = 3  # поставим постраничный вывод в один элемент

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


class FullNews(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    template_name = 'posts_full.html'
    context_object_name = 'posts'
    ordering = ['-article_time_in']
    permission_required = ('news.view_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    permission_required = ('news.view_post',)

    # кеширование до изменения объекта (метод get_object включительно):
    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует
        # # также. Он забирает значение по ключу, если его нет, то забирает None.
        # # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object()
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = NewsForm
    permission_required = ('news.add_post', 'news.change_post')

    # def post(self, request, *args, **kwargs):
    #     f = NewsForm(request.POST)
    #     post = f.save()
    #     new_post_categories = post.article_category.all()
    #
    #     list_of_users = []
    #     html_context = {'new_post': post, 'new_post_id': post.id, }
    #     for cat in new_post_categories:
    #         html_context['new_post_category'] = cat
    #         subs = Category.objects.get(category_name=cat).category_subscriber.all()
    #         for sub in subs:
    #             list_of_users.append(sub.email)
    #
    #     html_content = render_to_string('mail_subscription_update.html', html_context)
    #     msg = EmailMultiAlternatives(
    #         subject='Новая публикация на velosiped.test',
    #         from_email='testun_test@mail.ru',
    #         to=list_of_users
    #     )
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
    #     return redirect('post_detail', post.id)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/full/'
    permission_required = ('news.delete_post',)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = NewsForm
    permission_required = ('news.change_post', 'news.add_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('posts_full')
