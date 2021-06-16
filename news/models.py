from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

# TODO migrate all on PostgresSQL


# Create your models here.
class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Автор'))
    author_rating = models.IntegerField(default=0, verbose_name=_('Рейтинг автора'))

    # метод функционирует, но надо разобраться, как работает методы post_set/comment_set и aggregate:
    def update_rating(self):

        post_rat = self.posts.all().aggregate(post_rtg=Sum('article_rating'))
        # Почему posts а не post_set - смотри поле article_author в классе Post
        p_rat = 0
        p_rat += post_rat.get('post_rtg')

        comment_rat = self.author_user.comment_set.all().aggregate(comment_rtg=Sum('comment_rating'))
        c_rat = 0
        c_rat += comment_rat.get('comment_rtg')

        self.author_rating = (p_rat * 3) + c_rat
        self.save()

    def __str__(self):
        return self.author_user.username

    class Meta:
        verbose_name = _('Автор')
        verbose_name_plural = _('Авторы')


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True, verbose_name=_('Наименование категории'))
    category_subscriber = models.ManyToManyField(User, blank=True, verbose_name=_('Подписчик категории'))

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Post(models.Model):
    ARTICLE_TYPES = (
        ('news', 'Новости'), ('article', 'Статья')
    )
    article_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Автор статьи или новости'),
                                       related_name='posts')
    # добавлен related_name, чтобы изменить стандартный post_set
    article_choice = models.CharField(max_length=50, choices=ARTICLE_TYPES)
    article_time_in = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    article_category = models.ManyToManyField(Category, verbose_name=_('Категория публикации'))
    article_title = models.CharField(max_length=255, verbose_name=_('Название статьи или новости'))
    article_text = models.TextField(verbose_name=_('Основной текст статьи'))
    article_rating = models.IntegerField(default=0, verbose_name=_('Рейтинг публикации'))

    def like(self):
        self.article_rating += 1
        self.save()

    def dislike(self):
        self.article_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.article_title}: {self.article_text[:50]}...'

    # def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с
    # публикацией (настройка мигрировала в settings.ABSOLUTE_URL_OVERRIDES)
    #     return f'/news/{self.id}'

    class Meta:
        verbose_name = _('Публикация')
        verbose_name_plural = _('Публикации')

    # метод для кеширования до изменения объекта:
    def save(self, *args, **kwargs):
        """Переопределяем метод сохранения с очисткой кеша"""
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Комментируемый пост'))
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор коммента'))
    comment_text = models.TextField(verbose_name=_('Текст комментария'))
    comment_time_in = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    comment_rating = models.IntegerField(default=0, verbose_name=_('Рейтинг комментария'))

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f"{self.comment_text[0:15]}..."

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
