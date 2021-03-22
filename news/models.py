from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    author_rating = models.IntegerField(default=0, verbose_name='Рейтинг автора')

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
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True, verbose_name='Наименование категории')
    category_subscriber = models.ManyToManyField(User, blank=True, verbose_name="Подписчик категории")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    ARTICLE_TYPES = (
        ('news', 'Новости'), ('article', 'Статья')
    )
    article_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор статьи или новости',
                                       related_name='posts')
    # добавлен related_name, чтобы изменить стандартный post_set
    article_choice = models.CharField(max_length=50, choices=ARTICLE_TYPES)
    article_time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    article_category = models.ManyToManyField(Category, verbose_name='Категория публикации')
    article_title = models.CharField(max_length=255, verbose_name='Название статьи или новости')
    article_text = models.TextField(verbose_name='Основной текст статьи')
    article_rating = models.IntegerField(default=0, verbose_name='Рейтинг публикации')

    def like(self):
        self.article_rating += 1
        self.save()

    def dislike(self):
        self.article_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.article_title}: {self.article_text[:20]}...'

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'
    #  создаём категорию, к которой будет привязываться товар

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментируемый пост')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор коммента')
    comment_text = models.TextField(verbose_name='Текст комментария')
    comment_time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    comment_rating = models.IntegerField(default=0, verbose_name='Рейтинг комментария')

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'"{self.comment_text[0:15]}..." В публикации: "{self.comment_post.article_title}" ' \
               f'От автора: {self.comment_user.username}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
