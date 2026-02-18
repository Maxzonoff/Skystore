from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Contacts


def home(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact = Contacts.objects.create(
            name=name,
            phone=phone,
            message=message
        )

        return HttpResponse(f'Спасибо, {name}! Ваш номер телефона {phone} и сообщение {message} получены.')
    return render(request, 'catalog/contacts.html')
