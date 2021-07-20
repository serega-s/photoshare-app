from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.description