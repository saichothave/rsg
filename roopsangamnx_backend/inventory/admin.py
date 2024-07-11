from django.contrib import admin
from .models import Category, Product, Brand, ProductArticle, SubCategory, ProductColor, ProductSize, Section

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    model = Section
    list_display = [
        'name'
    ]
    ordering = ['name']
    search_fields = ['name']
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'section'
    ]
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['section']
    inlines = [SubCategoryInline]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category'
    ]
    search_fields = ['name']
    ordering = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'brand', 'size', 'color', 
        'section', 'category', 
        'subcategory', 'selling_price', 
        'inventory', 'barcode', 'is_multi_pack', 'multi_pack_quantity'
    )
    search_fields = ('name', 'brand__name', 'category__name', 'subcategory__name', 'barcode', 'color__color')
    list_filter = ('brand', 'category', 'subcategory', 'color', 'size', 'section')


class ProductColorAdmin(admin.ModelAdmin):
    model = ProductColor
    search_fields, ordering = ['color'], ['color']

class ProductSizeAdmin(admin.ModelAdmin):
    model = ProductSize
    search_fields, ordering = ['size'], ['size']

class ProductArticleAdmin(admin.ModelAdmin):
    model = ProductArticle
    search_fields, ordering = ['article'], ['article']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(Brand)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ProductArticle, ProductArticleAdmin)



