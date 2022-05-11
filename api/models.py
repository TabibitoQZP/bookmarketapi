from ast import operator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Book(models.Model):
    ISBN = models.CharField(max_length=20,primary_key=True)
    name=models.CharField(max_length=30)
    author=models.CharField(max_length=30)
    public=models.CharField(max_length=30)
    remain=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=7, decimal_places=2)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    realname=models.CharField(max_length=30)
    id=models.AutoField(primary_key=True)
    man=models.BooleanField()
    birth=models.DateField()

class Cargo(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateTimeField(default=timezone.now)
    price=models.DecimalField(max_digits=9,decimal_places=2)
    amount=models.PositiveBigIntegerField(default=0)
    status=models.CharField(max_length=1)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    def __str__(self):
        return self.book.name

class Bill(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateTimeField(default=timezone.now)
    earn=models.DecimalField(max_digits=9, decimal_places=2)