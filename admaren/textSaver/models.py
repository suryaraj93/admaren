from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Text(models.Model):
    text_title = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag, on_delete=CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text_title
