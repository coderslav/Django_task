"""Custom command ratings_reset.py for manage.py. Command reset to zero Ratings of all Authors

Exports
-------
BaseCommand from django.core.management.base:
    parent class for new class
Author from news.models:
    Author DB model of "news" app

Classes
----------
Command:
    Inherited class from BaseCommand
"""
from django.core.management.base import BaseCommand
from news.models import Author


class Command(BaseCommand):
    """
    Inherited class from BaseCommand for reset to zero (Ratings of all Authors) command

    Attributes
    ----------
    "override" help : str
        help message
    "override" requires_migrations_checks : bool
        check if all migrations are done

    Methods
    -------
    "override" handle(self, *args, **options)
        iterate all Author models and change rating for zero (if not zero already) + SUCCESS/ERROR message
    """

    help = 'Обнуляет рейтинг всех авторов'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        """iterate all Author models and change rating for zero (if not zero already) + SUCCESS/ERROR message"""
        self.stdout.write(self.style.WARNING('Do you really want reset ratings of all authors? yes/no'))
        answer = input()
        if answer.upper() == 'YES':
            for a_rating in Author.objects.all():
                if a_rating.author_rating != 0:
                    a_rating.author_rating = 0
                    a_rating.save()

                    self.stdout.write(self.style.SUCCESS(f'Successful reset of rating for {a_rating.author_user}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Error. Rating of {a_rating.author_user} is already equal 0'))
        elif answer.upper() == 'NO':
            self.stdout.write(self.style.MIGRATE_HEADING('Okay! Goodbye!'))
        else:
            self.stdout.write(self.style.ERROR('Input Error! Access denied! Type only "yes" or "no"'))
