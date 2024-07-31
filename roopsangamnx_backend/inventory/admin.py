from django.contrib import admin
from .models import Category, Product, Brand, ProductArticle, ProductVariant, SubCategory, ProductColor, ProductSize, Section
from unfold.admin import ModelAdmin


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class SectionAdmin(ModelAdmin):
    model = Section
    list_display = [
        'name'
    ]
    ordering = ['name']
    search_fields = ['name']
class CategoryAdmin(ModelAdmin):
    list_display = [
        'name',
        'section'
    ]
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['section']
    inlines = [SubCategoryInline]

class SubCategoryAdmin(ModelAdmin):
    list_display = [
        'name',
        'category'
    ]
    search_fields = ['name']
    ordering = ['name']

class ProductAdmin(ModelAdmin):
    list_display = (
        'name', 'brand', 'section', 'category', 
        'subcategory', 'is_multi_pack', 'multi_pack_quantity'
    )
    search_fields = ('name', 'brand__name', 'category__name', 'subcategory__name', 'barcode' )
    list_filter = ('brand', 'category', 'subcategory', 'section')


class ProductColorAdmin(ModelAdmin):
    model = ProductColor
    search_fields, ordering = ['color'], ['color']

class ProductSizeAdmin(ModelAdmin):
    model = ProductSize
    search_fields, ordering = ['size'], ['size']

class ProductArticleAdmin(ModelAdmin):
    model = ProductArticle
    search_fields, ordering = ['article'], ['article']

class ProductVariantAdmin(admin.ModelAdmin):
    # list_display = (
    #     'product__name', 'product__brand', 'product__section', 'product__category', 
    #     'product__subcategory', 'product__is_multi_pack', 'product__multi_pack_quantity'
    # )
    list_display = ('product_name', 'product_category', 'color', 'size', 'selling_price', 'inventory', )
    search_fields = ('product__name', 'product__barcode')
    # list_filter = ('product', 'mfd_date', 'size__size')
    list_filter = ('product__section', 'product__brand', 'product__category', 'product__subcategory', 'size')
    raw_id_fields = ('color', 'product')

    def product_name(self, obj):
        return obj.product.brand.name +" "+ obj.product.name
    
    def product_category(self, obj):
        return obj.product.category.name + " [" + obj.product.subcategory.name + "]"


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(Brand)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ProductArticle, ProductArticleAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)



