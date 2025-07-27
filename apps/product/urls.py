from django.urls import path
from .views import ProductCreate, ProductList, ProductUpdate, product_delete_func


urlpatterns = [
    path('list/', ProductList.as_view(template_name='product/list.html'), name='product_list'),
    path('create/', ProductCreate.as_view(template_name='product/create.html'), name='product_create'),
    path('<pk>/update/', ProductUpdate.as_view(template_name='product/create.html'), name='product_update'),
    path('<pk>/delete/', product_delete_func, name='product_delete'),
]
