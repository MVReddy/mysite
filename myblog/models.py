from __future__ import unicode_literals

from django.db import models

# Create your models here.


class DataStore(models.Model):
    name = models.CharField(max_length=100)
    data = models.FileField()
