from django.contrib import admin

from .models import Product, Entry

# Register your models here.
admin.site.register(Product)
admin.site.register(Entry)