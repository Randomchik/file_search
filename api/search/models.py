import uuid
from django.db import models

class Search(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255, null=True, blank=True)
    file_mask = models.CharField(max_length=255, null=True, blank=True)
    size_value = models.BigIntegerField(null=True, blank=True)
    size_operator = models.CharField(max_length=2, null=True, blank=True)
    creation_time_value = models.DateTimeField(null=True, blank=True)
    creation_time_operator = models.CharField(max_length=2, null=True, blank=True)
    finished = models.BooleanField(default=False)
    results = models.JSONField(default=list)
