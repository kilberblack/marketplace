from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class product(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    fabricante = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
