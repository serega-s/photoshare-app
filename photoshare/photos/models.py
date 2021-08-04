from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='photos')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    # card_image = models.ImageField(default='https://im0-tub-ru.yandex.net/i?id=a53f190616d5598d4d70d2488508ec89&n=13&exp=1')
    avatar = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username

User.profile = property(
    lambda u: Profile.objects.get_or_create(user=u)[0])
