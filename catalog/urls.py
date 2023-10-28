from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, contacts, ProductDetailView, ProductCreateView, ProductUpdateView, categories

app_name = CatalogConfig.name

urlpatterns = [
                  path('', ProductListView.as_view(), name='list'),
                  path('contacts/', contacts, name='contacts'),
                  path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
                  path('create/', ProductCreateView.as_view(), name='create_product'),
                  path('update/<int:pk>', ProductUpdateView.as_view(), name='update_product'),
                  path('categories/', categories, name='categories'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
