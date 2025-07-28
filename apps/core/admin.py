from django.contrib import admin
from apps.core.models import Company, Module


class CompanyAdmin(admin.ModelAdmin):
    pass

class ModuleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company, CompanyAdmin)
admin.site.register(Module, ModuleAdmin)
