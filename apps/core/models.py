from django.db import models


class BaseLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Module(BaseLog):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=16, primary_key=True)
    icon = models.CharField(max_length=32)
    path = models.CharField()

    def __str__(self):
        return self.name


class Company(BaseLog):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CompanyModule(BaseLog):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='company_modules')
