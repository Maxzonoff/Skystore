from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView, ArticlePublishView, ArticleUnpublishView,
)

app_name = BlogConfig.name

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("create/", ArticleCreateView.as_view(), name="article_create"),
    path("update/<int:pk>/", ArticleUpdateView.as_view(), name="article_update"),
    path("delete/<int:pk>/", ArticleDeleteView.as_view(), name="article_delete"),
    path('publish/<int:pk>/', ArticlePublishView.as_view(), name='article_publish'),
    path('unpublish/<int:pk>/', ArticleUnpublishView.as_view(), name='article_unpublish'),
]
