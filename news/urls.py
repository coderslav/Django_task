from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, FullNews, NewsDelete, NewsUpdate

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('search/', NewsSearch.as_view()),
    path('add/', NewsCreate.as_view(), name='post_create'),
    path('full/', FullNews.as_view(), name='posts_full'),
    path('delete/<int:pk>/', NewsDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='post_update'),
]
