import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_time = models.DateTimeField(default=timezone.now, db_index=True)
    modified_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True