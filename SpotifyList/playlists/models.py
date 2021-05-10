from django.db import models

# Create your models here.
class User(models.Model):
    token=models.CharField(max_length=256)
