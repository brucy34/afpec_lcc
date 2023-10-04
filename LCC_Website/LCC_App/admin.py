from django.contrib import admin
from .models import Category, Book, Event, Concurrent

# Register your models here

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Event)
admin.site.register(Concurrent)
