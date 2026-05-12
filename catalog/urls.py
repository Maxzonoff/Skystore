from django.urls import path

from .apps import CatalogConfig
from .views import (
    ContactsListView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView, UnpublishProductView, PublishProductView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("new/", ProductCreateView.as_view(), name="product_create"),
    path("update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("contacts/", ContactsListView.as_view(), name="contacts"),
    path('unpublish/<int:product_id>/', UnpublishProductView.as_view(), name='product_unpublish'),
    path('publish/<int:product_id>/', PublishProductView.as_view(), name='product_publish'),
]