from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.core.models import Company


class User(AbstractUser):
    class Roles(models.TextChoices):
        MANAGER = "manager", "Manager"
        USER = "user", "User"
        PUBLIC = "public", "Public"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(
        max_length=16,
        choices=Roles.choices,
        default=Roles.PUBLIC,
        null=False
    )
