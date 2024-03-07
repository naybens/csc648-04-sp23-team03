from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.contrib.auth.models import User


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now=True)


class Category(models.Model):
    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    text = models.CharField(max_length=32)


class Choice(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.CharField(max_length=32)
    is_picked = models.BooleanField(default=False)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(
        null=False, default='https://csc648whereweeatinmeow.s3.us-west-2.amazonaws.com/cat-1.png')
    restaurant_text = models.CharField(max_length=64)
    user_rating = models.IntegerField(default=0, blank=True, null=True)
    creation_datetime = models.DateTimeField(auto_now=True)
