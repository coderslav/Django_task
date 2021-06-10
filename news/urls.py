from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, FullNews, NewsDelete, NewsUpdate, upgrade_me, \
    subscribe_view
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', NewsList.as_view(), name='index'),
    path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('search/', NewsSearch.as_view()),
    path('add/', NewsCreate.as_view(), name='post_create'),
    # Page with cache:
    # path('full/', cache_page(60)(FullNews.as_view()), name='posts_full'),
    path('full/', FullNews.as_view(), name='posts_full'),
    path('delete/<int:pk>/', NewsDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='post_update'),
    path('upgrade/', upgrade_me, name='upgrade_user'),
    path('subscribe/', subscribe_view, name='subscribe'),
]
