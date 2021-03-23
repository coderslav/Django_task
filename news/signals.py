from django.template.loader import render_to_string
from .models import Post
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо
# передать также модель
@receiver(m2m_changed, sender=Post.article_category.through)
def notify_subscribers(sender, action, instance, **kwargs):
    if action == 'post_add':
        new_post_categories = instance.article_category.all()
        list_of_users = []
        html_context = {'new_post': instance, }
        for cat in new_post_categories:
            html_context['new_post_category'] = cat
            subs = cat.category_subscriber.all()
            for sub in subs:
                list_of_users.append(sub.email)
        html_content = render_to_string('mail_subscription_update.html', html_context)
        msg = EmailMultiAlternatives(
           subject='Новая публикация на velosiped.test',
           from_email='testun_test@mail.ru',
           to=list_of_users
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
