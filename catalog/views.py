from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ProductForm
from catalog.models import Contacts, Product
from django.contrib import messages


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет права отменять публикацию продукта')

        product.is_published = False
        product.save()
        messages.success(request, f'Продукт "{product.name}" снят с публикации')

        return redirect('catalog:product_detail', pk=product_id)


class PublishProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет права публиковать продукт')

        if product.is_published:
            messages.warning(request, f'Продукт "{product.name}" уже опубликован')
            return redirect('catalog:product_detail', pk=product_id)

        product.is_published = True
        product.save()
        messages.success(request, f'Продукт "{product.name}" опубликован')

        return redirect('catalog:product_detail', pk=product_id)


class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_published=True)[:6]
        return context


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        if self.request.user.has_perm('catalog.can_unpublish_product'):
            return Product.objects.all().order_by('-created_at')
        return Product.objects.filter(is_published=True).order_by('-created_at')


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if not obj.is_published and not self.request.user.has_perm('catalog.can_unpublish_product'):
            return PermissionDenied("Товар не найден или не опубликован")

        return obj


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        messages.success(self.request, 'Продукт успешно создан и отправлен на модерацию')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактировать продукт могут:
    1. Владелец продукта
    2. Администратор (superuser)
    """
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        """Проверка: пользователь - владелец продукта ИЛИ администратор"""
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.is_superuser

    def handle_no_permission(self):
        """Что делать, если нет прав"""
        messages.error(self.request, 'Редактировать может только владелец продукта или администратор')
        return redirect('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удалять продукт могут:
    1. Владелец продукта
    2. Модератор/администратор (имеющий право can_unpublish_product)
    3. Администратор (superuser)
    """
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        """Проверка прав на удаление"""
        product = self.get_object()
        user = self.request.user

        return (product.owner == user or
                user.has_perm('catalog.can_unpublish_product') or
                user.is_superuser)

    def handle_no_permission(self):
        """Если нет прав"""
        messages.error(self.request, 'У вас нет прав для удаления этого продукта')
        return redirect('catalog:product_list')


class ContactsListView(ListView):
    model = Contacts
    template_name = "catalog/contacts_list.html"

    def get(self, request, *args, **kwargs):
        """GET запрос - показываем страницу"""
        contacts_list = Contacts.objects.all()
        return render(request, self.template_name, {"contacts": contacts_list})

    def post(self, request, *args, **kwargs):
        """POST запрос - обрабатываем форму"""
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and phone:
            Contacts.objects.create(name=name, phone=phone, message=message or "")

            return HttpResponse(
                f"Спасибо, {name}! Ваш номер телефона {phone} и сообщение {message} получены."
            )
        else:
            return HttpResponse("Пожалуйста, заполните имя и телефон.")
