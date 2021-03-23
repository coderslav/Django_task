from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.

    class Meta:
        model = Post
        fields = ['article_title', 'article_text', 'article_category', 'article_author']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
