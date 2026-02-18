from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "image", "category", "price", "created_at", "updated_at",)
    list_filter = ("category",)
    search_fields = ("name", "description",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at",)
    list_filter = ("name",)
    search_fields = ("name", "description",)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "message", "created_at", "updated_at",)
    list_filter = ("name", "phone",)
    search_fields = ("name", "message",)
