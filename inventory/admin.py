from django.contrib import admin
from .models import Category, Product, Brand, SubCategory

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(SubCategory)

