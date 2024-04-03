import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('worker', 'Worker'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='worker')

    email = models.EmailField(unique=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
