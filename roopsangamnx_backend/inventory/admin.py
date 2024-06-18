from django.contrib import admin
from .models import Category, Product, Brand, SubCategory, ProductColor, ProductSize

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(Brand)
admin.site.register(SubCategory)


