from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("products/", views.products_list, name="products_list"),
    path("prod_detail/<int:pk>/", views.prod_detail, name="prod_detail"),
]
