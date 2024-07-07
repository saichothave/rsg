from django.contrib import admin
from .models import Category, Product, Brand, SubCategory, ProductColor, ProductSize, Section

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'brand', 'size', 'color', 
        'section', 'category', 
        'subcategory', 'selling_price', 
        'inventory', 'barcode', 'is_multi_pack', 'multi_pack_quantity'
    )
    search_fields = ('name', 'brand__name', 'category__name', 'subcategory__name', 'barcode', 'color__color')
    list_filter = ('brand', 'category', 'subcategory', 'color', 'size', 'section')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
admin.site.register(Brand)
admin.site.register(SubCategory)
admin.site.register(Section)



