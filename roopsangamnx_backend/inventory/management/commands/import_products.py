import os
import django
import json
from datetime import datetime
from django.core.exceptions import ValidationError

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from roopsangamnx_backend.models import Product, Section, Category, SubCategory, Brand, ProductArticle, ProductSize, ProductColor, ProductVariant

def import_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for product_data in data:
        try:
            section, _ = Section.objects.get_or_create(name=product_data['section'])
            category, _ = Category.objects.get_or_create(name=product_data['category'], section=section)
            subcategory, _ = SubCategory.objects.get_or_create(name=product_data['subcategory'], category=category)
            brand, _ = Brand.objects.get_or_create(name=product_data['brand'])
            article_no, _ = ProductArticle.objects.get_or_create(article=product_data['article_no'])
            
            product, created = Product.objects.get_or_create(
                id=product_data['id'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'barcode': product_data['barcode'],
                    'is_multi_pack': product_data['is_multi_pack'],
                    'multi_pack_quantity': product_data['multi_pack_quantity'],
                    'section': section,
                    'category': category,
                    'subcategory': subcategory,
                    'brand': brand,
                    'article_no': article_no,
                    'created_at': datetime.fromisoformat(product_data['created_at']),
                    'updated_at': datetime.fromisoformat(product_data['updated_at'])
                }
            )
            
            if not created:
                product.name = product_data['name']
                product.description = product_data['description']
                product.barcode = product_data['barcode']
                product.is_multi_pack = product_data['is_multi_pack']
                product.multi_pack_quantity = product_data['multi_pack_quantity']
                product.section = section
                product.category = category
                product.subcategory = subcategory
                product.brand = brand
                product.article_no = article_no
                product.created_at = datetime.fromisoformat(product_data['created_at'])
                product.updated_at = datetime.fromisoformat(product_data['updated_at'])
                product.save()
            
            for variant_data in product_data['variants']:
                size, _ = ProductSize.objects.get_or_create(size=variant_data['size'])
                color, _ = ProductColor.objects.get_or_create(color=variant_data['color'])
                
                variant, created = ProductVariant.objects.get_or_create(
                    id=variant_data['id'],
                    defaults={
                        'product': product,
                        'size': size,
                        'color': color,
                        'mfd_date': datetime.fromisoformat(variant_data['mfd_date']),
                        'buying_price': variant_data['buying_price'],
                        'selling_price': variant_data['selling_price'],
                        'applicable_gst': variant_data['applicable_gst'],
                        'inventory': variant_data['inventory'],
                        'created_at': datetime.fromisoformat(variant_data['created_at']),
                        'updated_at': datetime.fromisoformat(variant_data['updated_at'])
                    }
                )
                
                if not created:
                    variant.product = product
                    variant.size = size
                    variant.color = color
                    variant.mfd_date = datetime.fromisoformat(variant_data['mfd_date'])
                    variant.buying_price = variant_data['buying_price']
                    variant.selling_price = variant_data['selling_price']
                    variant.applicable_gst = variant_data['applicable_gst']
                    variant.inventory = variant_data['inventory']
                    variant.created_at = datetime.fromisoformat(variant_data['created_at'])
                    variant.updated_at = datetime.fromisoformat(variant_data['updated_at'])
                    variant.save()
        
        except ValidationError as e:
            print(f"Validation error for product {product_data['name']}: {e}")
        except Exception as e:
            print(f"Error importing product {product_data['name']}: {e}")

if __name__ == "__main__":
    import_data_from_json('path_to_your_json_file.json')
