import json
from django.core.management.base import BaseCommand
from inventory.models  import ProductVariant, Product, Section, Category, SubCategory, Brand, ProductArticle

class Command(BaseCommand):
    help = 'Export ProductVariant data to JSON file'

    def handle(self, *args, **kwargs):
        products = Product.objects.prefetch_related(
            'variants', 'section', 'category', 'subcategory', 'brand', 'article_no'
        ).all()

        data = []
        for product in products:
            product_data = {
                # 'id': product.id,
                'variants': [
                    {
                        # 'id': variant.id,
                        'size': {
                            # 'id': variant.size.id,
                            # 'created_at': variant.size.created_at.isoformat(),
                            # 'updated_at': variant.size.updated_at.isoformat(),
                            'size': variant.size.size
                        } if variant.size else None,
                        'color': {
                            # 'id': variant.color.id,
                            # 'created_at': variant.color.created_at.isoformat(),
                            # 'updated_at': variant.color.updated_at.isoformat(),
                            'color': variant.color.color
                        } if variant.color else None,
                        'mfd_date': variant.mfd_date.isoformat(),
                        'buying_price': str(variant.buying_price),
                        'selling_price': str(variant.selling_price),
                        'applicable_gst': str(variant.applicable_gst),
                        'inventory': variant.inventory
                    } for variant in product.variants.all()
                ],
                'section': {
                    # 'id': product.section.id,
                    'name': product.section.name,
                    # 'created_at': product.section.created_at.isoformat(),
                    # 'updated_at': product.section.updated_at.isoformat()
                } if product.section else None,
                'category': {
                    # 'id': product.category.id,
                    'name': product.category.name,
                    'section': {
                        # 'id': product.category.section.id,
                        'name': product.category.section.name,
                        # 'created_at': product.category.section.created_at.isoformat(),
                        # 'updated_at': product.category.section.updated_at.isoformat()
                    } if product.category and product.category.section else None,
                    # 'created_at': product.category.created_at.isoformat(),
                    # 'updated_at': product.category.updated_at.isoformat()
                } if product.category else None,
                'subcategory': {
                    # 'id': product.subcategory.id,
                    'name': product.subcategory.name,
                    'category': {
                        # 'id': product.subcategory.category.id,
                        'name': product.subcategory.category.name,
                        'section': {
                            # 'id': product.subcategory.category.section.id,
                            'name': product.subcategory.category.section.name,
                            # 'created_at': product.subcategory.category.section.created_at.isoformat(),
                            # 'updated_at': product.subcategory.category.section.updated_at.isoformat()
                        } if product.subcategory and product.subcategory.category and product.subcategory.category.section else None,
                        # 'created_at': product.subcategory.category.created_at.isoformat(),
                        # 'updated_at': product.subcategory.category.updated_at.isoformat()
                    } if product.subcategory and product.subcategory.category else None,
                    # 'created_at': product.subcategory.created_at.isoformat(),
                    # 'updated_at': product.subcategory.updated_at.isoformat()
                } if product.subcategory else None,
                'brand': {
                    # 'id': product.brand.id,
                    'name': product.brand.name,
                    # 'created_at': product.brand.created_at.isoformat(),
                    # 'updated_at': product.brand.updated_at.isoformat()
                } if product.brand else None,
                'article_no': {
                    # 'id': product.article_no.id,
                    # 'created_at': product.article_no.created_at.isoformat(),
                    # 'updated_at': product.article_no.updated_at.isoformat(),
                    'article': product.article_no.article
                } if product.article_no else None,
                # 'created_at': product.created_at.isoformat(),
                # 'updated_at': product.updated_at.isoformat(),
                'name': product.name,
                'image': product.image.url if product.image else None,
                'description': product.description,
                'barcode': product.barcode,
                'is_multi_pack': product.is_multi_pack,
                'multi_pack_quantity': product.multi_pack_quantity
            }
            data.append(product_data)

        with open('product_variants.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully exported ProductVariant data to product_variants.json'))
