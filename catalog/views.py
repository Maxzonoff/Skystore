from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.models import Contacts, Product


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "image", "category", "price"]
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "image", "category", "price"]
    success_url = reverse_lazy("catalog:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class ContactsListView(ListView):
    model = Contacts
    template_name = 'catalog/contacts_list.html'

    def get(self, request, *args, **kwargs):
        """GET запрос - показываем страницу"""
        contacts_list = Contacts.objects.all()
        return render(request, self.template_name, {'contacts': contacts_list})

    def post(self, request, *args, **kwargs):
        """POST запрос - обрабатываем форму"""
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and phone:
            Contacts.objects.create(
                name=name,
                phone=phone,
                message=message or ''
            )

            return HttpResponse(
                f"Спасибо, {name}! Ваш номер телефона {phone} и сообщение {message} получены."
            )
        else:
            return HttpResponse("Пожалуйста, заполните имя и телефон.")