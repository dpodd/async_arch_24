import uuid

from django.db import models

from users.models import User


class Task(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='assigned_tasks', null=True, blank=True
    )

    def __str__(self):
        return self.title
