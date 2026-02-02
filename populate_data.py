"""
Script to populate sample data for Luxura jewelry store
Run with: python manage.py shell < populate_data.py
"""

from store.models import Category, Product
from django.utils.text import slugify
import os

# Create sample categories
categories_data = [
    {
        'name': 'Rings',
        'description': 'Elegant rings for every occasion'
    },
    {
        'name': 'Necklaces',
        'description': 'Beautiful necklaces that make a statement'
    },
    {
        'name': 'Earrings',
        'description': 'Stunning earrings to complete your look'
    },
    {
        'name': 'Bracelets',
        'description': 'Exquisite bracelets for any style'
    },
    {
        'name': 'Beauty Products',
        'description': 'Premium beauty and skincare products'
    }
]

print("Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'slug': slugify(cat_data['name']),
            'description': cat_data['description']
        }
    )
    if created:
        print(f"✓ Created category: {category.name}")
    else:
        print(f"✓ Category already exists: {category.name}")

# Get all categories
rings = Category.objects.get(name='Rings')
necklaces = Category.objects.get(name='Necklaces')
earrings = Category.objects.get(name='Earrings')
bracelets = Category.objects.get(name='Bracelets')
beauty = Category.objects.get(name='Beauty Products')

# Create sample products
products_data = [
    # Rings
    {
        'name': 'Diamond Solitaire Ring',
        'category': rings,
        'description': 'Timeless diamond solitaire ring crafted in 18K gold. The perfect symbol of elegance and sophistication.',
        'price': '2499.99',
        'original_price': '3299.99',
        'is_featured': True,
        'is_new': False,
        'stock': 5
    },
    {
        'name': 'Emerald and Gold Ring',
        'category': rings,
        'description': 'Stunning emerald gemstone set in luxurious gold with intricate detailing. A true showstopper.',
        'price': '1899.99',
        'original_price': '2299.99',
        'is_featured': True,
        'is_new': True,
        'stock': 8
    },
    {
        'name': 'Sapphire Engagement Ring',
        'category': rings,
        'description': 'Exquisite sapphire center stone with diamond accents. A unique and timeless piece.',
        'price': '2199.99',
        'is_featured': False,
        'is_new': True,
        'stock': 3
    },
    
    # Necklaces
    {
        'name': 'Gold Pearl Pendant',
        'category': necklaces,
        'description': 'Luxurious pearl pendant suspended from a delicate gold chain. Perfect for any occasion.',
        'price': '899.99',
        'original_price': '1199.99',
        'is_featured': True,
        'is_new': False,
        'stock': 12
    },
    {
        'name': 'Crystal Charm Necklace',
        'category': necklaces,
        'description': 'Elegant crystal charm on a fine gold chain. A versatile piece that complements any outfit.',
        'price': '599.99',
        'is_featured': False,
        'is_new': True,
        'stock': 15
    },
    {
        'name': 'Diamond Tennis Necklace',
        'category': necklaces,
        'description': 'Classic tennis necklace featuring brilliant diamonds. The ultimate luxury statement piece.',
        'price': '3999.99',
        'original_price': '4999.99',
        'is_featured': True,
        'is_new': False,
        'stock': 2
    },
    
    # Earrings
    {
        'name': 'Diamond Stud Earrings',
        'category': earrings,
        'description': 'Timeless diamond studs that sparkle with every move. A classic investment piece.',
        'price': '1499.99',
        'original_price': '1999.99',
        'is_featured': True,
        'is_new': False,
        'stock': 10
    },
    {
        'name': 'Pearl Drop Earrings',
        'category': earrings,
        'description': 'Elegant pearl drop earrings with gold accents. Perfect for formal occasions.',
        'price': '699.99',
        'is_featured': False,
        'is_new': True,
        'stock': 8
    },
    {
        'name': 'Rose Gold Chandelier Earrings',
        'category': earrings,
        'description': 'Glamorous rose gold chandelier earrings with intricate details. A show-stopping accessory.',
        'price': '899.99',
        'original_price': '1199.99',
        'is_featured': False,
        'is_new': True,
        'stock': 6
    },
    
    # Bracelets
    {
        'name': 'Diamond Tennis Bracelet',
        'category': bracelets,
        'description': 'Luxurious diamond tennis bracelet that sparkles beautifully on the wrist.',
        'price': '2999.99',
        'original_price': '3999.99',
        'is_featured': True,
        'is_new': False,
        'stock': 4
    },
    {
        'name': 'Gold Bangle Bracelet',
        'category': bracelets,
        'description': 'Classic gold bangle bracelet with elegant details. A timeless accessory.',
        'price': '799.99',
        'is_featured': False,
        'is_new': True,
        'stock': 20
    },
    {
        'name': 'Sapphire and Diamond Bracelet',
        'category': bracelets,
        'description': 'Stunning bracelet combining sapphires and diamonds for a breathtaking look.',
        'price': '2499.99',
        'original_price': '3199.99',
        'is_featured': True,
        'is_new': True,
        'stock': 5
    },
    
    # Beauty Products
    {
        'name': 'Luxury Face Serum',
        'category': beauty,
        'description': 'Premium anti-aging face serum with gold particles. Leaves skin glowing and radiant.',
        'price': '129.99',
        'original_price': '179.99',
        'is_featured': False,
        'is_new': True,
        'stock': 50
    },
    {
        'name': 'Hydrating Face Cream',
        'category': beauty,
        'description': 'Luxurious moisturizing cream infused with precious minerals and gold.',
        'price': '99.99',
        'is_featured': True,
        'is_new': False,
        'stock': 60
    },
    {
        'name': 'Premium Lipstick Set',
        'category': beauty,
        'description': 'Collection of luxury lipsticks in stunning shades. Long-lasting and vibrant.',
        'price': '89.99',
        'original_price': '129.99',
        'is_featured': False,
        'is_new': True,
        'stock': 40
    },
]

print("\nCreating products...")
for prod_data in products_data:
    category = prod_data.pop('category')
    slug = slugify(prod_data['name'])
    
    product, created = Product.objects.get_or_create(
        slug=slug,
        defaults={
            'category': category,
            **prod_data
        }
    )
    
    if created:
        print(f"✓ Created product: {product.name}")
    else:
        print(f"✓ Product already exists: {product.name}")

print("\n✅ Sample data population complete!")
print(f"Total categories: {Category.objects.count()}")
print(f"Total products: {Product.objects.count()}")
