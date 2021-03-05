from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
class NewsFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля по которым будет фильтроваться (т.е. подбираться)
    # информация о товарах
    class Meta:
        model = Post
        fields = {
            'article_title': ['icontains'],  # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то что
            # запросил пользователь
            'article_author': [],
            'article_time_in': ['date'],
        }
