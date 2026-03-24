from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("blog/create", ArticleCreateView.as_view(), name="article_create"),
    path("blog/<int:pk>/update", ArticleUpdateView.as_view(), name="article_update"),
    path("blog/<int:pk>/delete", ArticleDeleteView.as_view(), name="article_delete")
]
