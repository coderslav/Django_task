from django.forms import ModelForm, BooleanField
from .models import Post


# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.

    class Meta:
        model = Post
        fields = ['article_title', 'article_text', 'article_category', 'article_author']
