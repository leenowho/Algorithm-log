from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Category


class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    interested_categories = models.ManyToManyField(Category, related_name='interested_users')
    chatbot_history = models.JSONField(default=list, blank=True, null=True)
