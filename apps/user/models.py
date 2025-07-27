from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        MANAGER = "manager", "Manager"
        USER = "user", "User"
        PUBLIC = "public", "Public"
    
    role = models.CharField(
        max_length=16,
        choices=Roles.choices,
        default=Roles.PUBLIC,
        null=False
    )
