
from django.urls import path

from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleDelete, ArticleUpdate

urlpatterns = [
    path('news/', NewsList.as_view(), name='post_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='post_search'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete')
]