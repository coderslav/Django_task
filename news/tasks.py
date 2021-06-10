from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from .models import Post, User
from django.template.loader import render_to_string
from datetime import datetime, timedelta


@shared_task
def hello():
    print("Hello, world!")


@shared_task
def printer(n: int):
    for i in range(n):
        time.sleep(1)
        print(i+1)


@shared_task
def cat_update_notifier(list_of_users: list, html_content):
    msg = EmailMultiAlternatives(
        subject='Новая публикация на velosiped.test',
        from_email='testun_test@mail.ru',
        to=list_of_users
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def action():
    new_posts = Post.objects.all().filter(article_time_in__gt=datetime.now() - timedelta(days=7))
    list_of_emails = []
    for user in User.objects.all():
        list_of_emails.append(user.email)
    html_context = {'new_posts': new_posts}
    html_content = render_to_string('mail_week_notification.html', html_context)
    msg = EmailMultiAlternatives(
        subject='Новые публикации на velosiped.test за 7 дней',
        from_email='testun_test@mail.ru',
        to=list_of_emails
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
