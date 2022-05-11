from django.contrib import admin

from .models import Book, Profile, Cargo, Bill

# Register your models here.
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(Cargo)
admin.site.register(Bill)