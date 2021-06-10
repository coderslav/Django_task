"""Custom command category_reset.py for manage.py. Reset command for all articles from selected category

Exports
-------
BaseCommand from django.core.management.base:
    parent command class for new command class
Category from news.models:
    Category DB model of "news" app
ObjectDoesNotExist from django.core.exceptions
    ObjectDoesNotExist exception for catching

Classes
----------
Command:
    Inherited class from BaseCommand
"""
from django.core.management.base import BaseCommand
from news.models import Category
from django.core.exceptions import ObjectDoesNotExist
from news.models import Post


class Command(BaseCommand):
    """
        Inherited class from BaseCommand class for resetting all articles from selected category

        Attributes
        ----------
        "override" help : str
            help message
        "override" requires_migrations_checks : bool
            check if all migrations are done

        Methods
        -------
        "override" handle(self, *args, **options)
            delete all related Post objects from target category by ".post_set.all().delete()" methods
        """
    help = "Command for resetting all articles from selected category"
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Which category do you want to reset?'))
        cat_input = input()
        try:
            # 3 варианта решения:
            # 1. Достаю (через Category model) все посты нужной категории через обратную связь (post_set)
            posts_len = len(Category.objects.get(category_name=cat_input).post_set.all())
            # 2. Достаю (через Post model) все посты нужной категории через "что-то похожее на обратную связь"
            # posts_len = len(Post.objects.filter(article_category__category_name=cat_input))
            # 3. Сначала нахожу нужную модель категории, потом фильтрую посты по id найденной модели
            # category = Category.objects.get(category_name=cat_input)
            # posts_len = len(Post.objects.filter(article_category=category.id))
            self.stdout.write(self.style.WARNING(f'You will delete all articles from category "{cat_input}". '
                                                 f'Are you sure? yes/no'))
            answer = input()
            if answer.lower() == 'yes':
                Category.objects.get(category_name=cat_input).post_set.all().delete()
                self.stdout.write(self.style.SUCCESS(f'All articles ({posts_len}) from "{cat_input}" '
                                                     f'was successfully deleted!'))
            elif answer.lower() == 'no':
                self.stdout.write(self.style.SUCCESS('Good decision!'))
            else:
                self.stdout.write(self.style.ERROR('Input Error! Type only "yes" or "no"'))
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Error! Category "{cat_input}" does not exist'))
