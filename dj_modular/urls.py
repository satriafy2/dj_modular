"""
URL configuration for dj_modular project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from apps.core.views import CompanyModuleList, ModuleList, add_company_module, remove_company_module
from apps.user.views import UserLoginView, UserLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', CompanyModuleList.as_view(template_name='core/home.html'), name='home'),
    path('module/', ModuleList.as_view(template_name='core/module_list.html'), name='module_list'),
    path('module/<str:module_code>/add/', add_company_module, name='module_add'),
    path('module/<pk>/remove/', remove_company_module, name='module_remove'),
    path('product/', include('apps.product.urls')),
]
