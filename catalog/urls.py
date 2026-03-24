from django.urls import path
from .apps import CatalogConfig
from .views import HomeView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ContactsListView

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("products/", ProductListView.as_view(), name="product_list"),
    path("product_detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("new", ProductCreateView.as_view(), name="product_create"),
    path("product_update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("product_delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("contacts/", ContactsListView.as_view(), name="contacts"),
]
