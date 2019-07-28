# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified_at = models.DateTimeField(default=timezone.now)
    author = models.TextField(blank=True)
    description = models.TextField(blank=True)
    size = models.UUIDField(default=uuid.uuid4)


class Deps(models.Model):
    pkg = models.ForeignKey(
        'Package', on_delete=models.CASCADE, null=True, related_name='dep_edge')
    dep = models.ForeignKey('Package', on_delete=models.PROTECT)
