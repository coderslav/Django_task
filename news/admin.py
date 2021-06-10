from django.contrib import admin
from .models import *


# делаем функцию для кастомизации "action" кнопки (для выделенных галочками объектов)
# model_admin - сюда подается любой из классов кастомизации админки
# request — объект хранящий информацию о запросе
# queryset — грубо говоря набор объектов, которых мы выделили галочками в админке
def nullify_rating(model_admin, request, queryset):
    queryset.update(comment_rating=0)


# описание для более понятного представления в админ панели задаётся, как будто это объект
nullify_rating.short_description = 'Обнулить рейтинг'


class CommentAdmin(admin.ModelAdmin):
    """Представление в админке всех полей модели Comment в виде таблицы и не только"""
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # генерируем список имён всех полей для более красивого отображения
    list_display = [field.name for field in Comment._meta.get_fields()]
    #  а также добавляем фильтры
    list_filter = ('comment_post', 'comment_rating', 'comment_time_in')
    # тут интегрируем поисковую строку, а в списке (или во множестве) указываем по каким полям хотим сикать
    # Foreign поля нужно указывать в формате: '<нужное поле>__<поле в связанной модели>'
    search_fields = ('comment_post__article_title', 'comment_rating', 'comment_time_in')
    # создаем кастомную "action" кнопку
    actions = [nullify_rating]


class PostAdmin(admin.ModelAdmin):
    """Представление в админке всех полей модели Post в виде таблицы и не только"""
    # идентичная процедура, только убираем связанные поля с Post от других моделей
    list_display = [field.name for field in Post._meta.get_fields()
                    if field.name not in ['article_category', 'comment']]


class CategoryAdmin(admin.ModelAdmin):
    """Представление в админке всех полей модели Category в виде таблицы и не только"""
    # идентичная процедура, только убираем связанные поля с Category от других моделей
    list_display = [field.name for field in Category._meta.get_fields()
                    if field.name not in ['category_subscriber', 'post']]


class AuthorAdmin(admin.ModelAdmin):
    """Представление в админке всех полей модели Author в виде таблицы и не только"""
    # идентичная процедура, только убираем связанные поля с Author от других моделей
    list_display = [field.name for field in Author._meta.get_fields()
                    if field.name != 'posts']


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.unregister(Author) чтобы "РАЗрегистрировать" модель
