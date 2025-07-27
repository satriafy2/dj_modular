from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from apps.product.models import Product
from apps.user.models import User


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    ordering = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allow_modify'] = False
        context['allow_delete'] = False

        if self.request.user.role in [User.Roles.MANAGER, User.Roles.USER]:
            context['allow_modify'] = True
        if self.request.user.role in [User.Roles.MANAGER]:
            context['allow_delete'] = True

        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('limit', 10)

    def get_queryset(self):
        queryset =  super().get_queryset()
        return queryset.filter(deleted_at__isnull=True)

class ProductCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = [
        'name',
        'product_code',
        'price',
        'stock'
    ]
    success_url = reverse_lazy('product_list')
    success_message = 'Product %(name)s created successfully'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'CREATE PRODUCT'
        return ctx

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in [User.Roles.MANAGER, User.Roles.USER]:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

class ProductUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = [
        'name',
        'product_code',
        'price',
        'stock'
    ]
    success_url = reverse_lazy('product_list')
    success_message = 'Product %(name)s updated successfully'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'UPDATE PRODUCT'
        return ctx

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in [User.Roles.MANAGER, User.Roles.USER]:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

def product_delete_func(request, pk):
    if request.user.role not in [User.Roles.MANAGER]:
        raise PermissionDenied()

    if request.method != 'POST':
        raise PermissionDenied()

    try:
        product = get_object_or_404(Product, id=pk)
        product.deleted_at = datetime.now()
        product.save()
        messages.success(request, 'Product {} deleted successfully'.format(product.name))
    except Exception as e:
        print(e)
        messages.error(request, 'Unknown Error')

    return redirect(reverse_lazy('product_list'))
