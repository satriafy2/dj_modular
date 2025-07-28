import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, BadRequest
from django.forms.models import model_to_dict
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from apps.core.models import Company, CompanyModule, Module
from apps.user.models import User


class ModuleList(LoginRequiredMixin, ListView):
    model = Module
    # context_object_name = 'modules'
    ordering = 'created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted_at__isnull=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_company = self.request.user.company
        queryset_cm = CompanyModule.objects.filter(company=user_company, deleted_at__isnull=True).all()
        installed_modules = [a.module.code for a in queryset_cm]

        ctx['modules'] = []
        for obj in ctx['object_list']:
            dict_module = model_to_dict(
                obj, fields=['name', 'code', 'path', 'icon']
            )

            if obj.code in installed_modules:
                company_module = obj.company_modules.filter(company=user_company).first()
                dict_module['join_id'] = company_module.id
                dict_module['installed'] = True
            else:
                dict_module['join_id'] = None
                dict_module['installed'] = False
            ctx['modules'].append(dict_module)
        
        return ctx
    

class CompanyModuleList(LoginRequiredMixin, ListView):
    model = CompanyModule
    context_object_name = 'objs'
    ordering = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        user_company = self.request.user.company
        return queryset.filter(deleted_at__isnull=True, company=user_company)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allow_modify'] = False
        if self.request.user.role in [User.Roles.MANAGER]:
            context['allow_modify'] = True

        return context
    

def add_company_module(request, module_code):
    if request.user.role not in [User.Roles.MANAGER]:
        raise PermissionDenied()

    if request.method != 'POST':
        raise PermissionDenied()

    company = request.user.company
    module = Module.objects.filter(code=module_code).first()
    if not module:
        raise BadRequest()
    
    company_module = CompanyModule.objects.filter(
        company=company,
        module=module
    ).first()

    if not company_module:
        company_module = CompanyModule(company=company, module=module)
    else:
        company_module.deleted_at = None
    
    company_module.save()
    messages.success(request, 'Module {} installed successfully'.format(module.name))
    return redirect(reverse_lazy('module_list'))


def remove_company_module(request, pk):
    if request.user.role not in [User.Roles.MANAGER]:
        raise PermissionDenied()

    if request.method != 'POST':
        raise PermissionDenied()
    
    try:
        company_module = get_object_or_404(CompanyModule, id=pk)
        company_module.deleted_at = datetime.now()
        company_module.save()
        messages.success(request, 'Module {} has been uninstalled'.format(company_module.module.name))
    except Exception as e:
        print(e)
        messages.error(request, 'Unknown Error')
    
    return redirect(reverse_lazy('module_list'))


    