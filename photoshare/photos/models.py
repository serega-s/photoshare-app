from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    @property
    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'Comment by {self.user}'
