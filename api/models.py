from django.db import models

# Create your models here.

class Book(models.Model):
    ISBN = models.CharField(max_length=20,primary_key=True)
    name=models.CharField(max_length=30)
    author=models.CharField(max_length=30)
    public=models.CharField(max_length=30)
    remain=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=7, decimal_places=2)