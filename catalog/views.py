from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from catalog.models import Product, Version
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory


# Create your views here.
# def index(request):
#     product_list = Product.objects.all()
#     context = {
#         'object_list': product_list,
#         'title': 'Каталог продуктов'
#     }
#     return render(request, 'catalog/index.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone} {message}')
        Category.objects.create(name=name, description=message)

    context = {
        'title': ' Контактная информация',
    }

    return render(request, 'catalog/contacts.html', context)


# def product(request, pk):
#     context = {
#         'object': Product.objects.get(pk=pk)
#     }
#
#     return render(request, 'catalog/product.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormSet(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']

        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)
