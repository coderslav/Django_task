from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    author_rating = models.IntegerField(default=0, verbose_name='Рейтинг автора')

    def update_rating(self):
        self.author_rating = (Post.article_rating * 3) + Comment.comment_rating
        self.save()

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    ARTICLE_TYPES = (
        ('news', 'Новости'), ('article', 'Статья')
    )
    article_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор статьи или новости')
    article_choice = models.CharField(max_length=50, choices=ARTICLE_TYPES)
    article_time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    article_category = models.ManyToManyField(Category, verbose_name='Категория публикации')
    article_title = models.CharField(max_length=255, verbose_name='Название статьи или новости')
    article_text = models.TextField(verbose_name='Основной текст статьи')
    article_rating = models.IntegerField(default=0, verbose_name='Рейтинг публикации')

    def like(self):
        self.article_rating = +1
        self.save()

    def dislike(self):
        self.article_rating = -1
        self.save()

    def preview(self):
        return self.article_text[0:124] + '...'

    def __str__(self):
        return self.article_title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментируемый пост')
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор коммента')
    comment_text = models.TextField(verbose_name='Текст комментария')
    comment_time_in = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    comment_rating = models.IntegerField(default=0, verbose_name='Рейтинг комментария')

    def like(self):
        self.comment_rating = +1
        self.save()

    def dislike(self):
        self.comment_rating = -1
        self.save()

    def __str__(self):
        return self.comment_post.article_title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
