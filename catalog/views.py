from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Contacts, Product


def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "catalog/home.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        contact = Contacts.objects.create(name=name, phone=phone, message=message)

        return HttpResponse(
            f"Спасибо, {name}! Ваш номер телефона {phone} и сообщение {message} получены."
        )
    return render(request, "catalog/contacts.html")


def products_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "catalog/products_list.html", context)


def prod_detail(request, pk):
    prod = Product.objects.get(pk=pk)
    context = {"prod": prod}
    return render(request, "catalog/prod_detail.html", context)
