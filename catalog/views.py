from django.shortcuts import render
from catalog.models import Product


# Create your views here.
def index(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Каталог продуктов'
    }
    return render(request, 'catalog/index.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone} {message}')
    context = {
        'title': ' Контактная информация',
    }

    return render(request, 'catalog/contacts.html', context)


def product(request, pk):
    context = {
        'object': Product.objects.get(pk=pk)
    }

    return render(request, 'catalog/product.html', context)
