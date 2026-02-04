#!/usr/bin/env python3
"""
Update KIRAA Jewelry Store Products
Remove beauty products and add more jewelry items with real images
"""

import os
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewelry_shop.settings')
django.setup()

from store.models import Category, Product

def remove_beauty_products():
    """Remove all beauty products from the store"""
    print("🧼 Removing beauty products...")
    
    # Remove beauty-related categories and their products
    beauty_keywords = ['beauty', 'skincare', 'cosmetic', 'makeup', 'cream', 'lotion', 'serum']
    
    for keyword in beauty_keywords:
        categories = Category.objects.filter(name__icontains=keyword)
        for category in categories:
            print(f"   Removing category: {category.name}")
            category.delete()
    
    # Remove individual beauty products that might be in other categories
    products = Product.objects.all()
    for product in products:
        if any(keyword in product.name.lower() or keyword in product.description.lower() 
               for keyword in beauty_keywords):
            print(f"   Removing product: {product.name}")
            product.delete()
    
    print("✅ Beauty products removed successfully!")

def create_jewelry_categories():
    """Create proper jewelry categories"""
    print("💎 Creating jewelry categories...")
    
    categories_data = [
        {
            'name': 'Diamond Rings',
            'slug': 'diamond-rings',
            'description': 'Exquisite diamond engagement and wedding rings'
        },
        {
            'name': 'Gold Necklaces',
            'slug': 'gold-necklaces', 
            'description': 'Elegant gold necklaces and pendants'
        },
        {
            'name': 'Pearl Jewelry',
            'slug': 'pearl-jewelry',
            'description': 'Classic and modern pearl accessories'
        },
        {
            'name': 'Silver Earrings',
            'slug': 'silver-earrings',
            'description': 'Beautiful silver and sterling silver earrings'
        },
        {
            'name': 'Bracelets',
            'slug': 'bracelets',
            'description': 'Stunning bracelets and bangles'
        },
        {
            'name': 'Wedding Jewelry',
            'slug': 'wedding-jewelry',
            'description': 'Complete bridal and wedding jewelry sets'
        },
        {
            'name': 'Men\'s Jewelry',
            'slug': 'mens-jewelry',
            'description': 'Sophisticated jewelry collection for men'
        }
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': cat_data['slug'],
                'description': cat_data['description']
            }
        )
        if created:
            print(f"   ✨ Created category: {category.name}")
        else:
            print(f"   📝 Category already exists: {category.name}")

def add_jewelry_products():
    """Add comprehensive jewelry product catalog"""
    print("💍 Adding jewelry products...")
    
    # Get categories
    diamond_rings = Category.objects.get(name='Diamond Rings')
    gold_necklaces = Category.objects.get(name='Gold Necklaces')
    pearl_jewelry = Category.objects.get(name='Pearl Jewelry')
    silver_earrings = Category.objects.get(name='Silver Earrings')
    bracelets = Category.objects.get(name='Bracelets')
    wedding_jewelry = Category.objects.get(name='Wedding Jewelry')
    mens_jewelry = Category.objects.get(name='Men\'s Jewelry')
    
    # Jewelry products with real image URLs
    products_data = [
        # Diamond Rings
        {
            'name': 'Classic Solitaire Diamond Ring',
            'slug': 'classic-solitaire-diamond-ring',
            'description': 'Timeless 1-carat diamond solitaire ring in 18K white gold setting. Perfect for engagements and special occasions.',
            'category': diamond_rings,
            'price': Decimal('45000'),
            'original_price': Decimal('52000'),
            'image': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&h=800&fit=crop',
            'stock': 5,
            'is_featured': True
        },
        {
            'name': 'Vintage Halo Diamond Ring',
            'slug': 'vintage-halo-diamond-ring',
            'description': 'Elegant vintage-inspired halo diamond ring with intricate detailing and side stones.',
            'category': diamond_rings,
            'price': Decimal('38000'),
            'original_price': Decimal('42000'),
            'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop',
            'stock': 8,
            'is_featured': True
        },
        {
            'name': 'Three Stone Diamond Ring',
            'slug': 'three-stone-diamond-ring',
            'description': 'Sophisticated three-stone diamond ring representing past, present, and future.',
            'category': diamond_rings,
            'price': Decimal('55000'),
            'original_price': Decimal('62000'),
            'image': 'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&h=800&fit=crop',
            'stock': 3
        },
        
        # Gold Necklaces
        {
            'name': 'Delicate Gold Chain Necklace',
            'slug': 'delicate-gold-chain-necklace',
            'description': 'Fine 18K gold chain necklace perfect for layering or wearing alone.',
            'category': gold_necklaces,
            'price': Decimal('15000'),
            'original_price': Decimal('18000'),
            'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop',
            'stock': 12,
            'is_featured': True
        },
        {
            'name': 'Gold Heart Pendant Necklace',
            'slug': 'gold-heart-pendant-necklace',
            'description': 'Romantic 22K gold heart pendant on delicate chain, perfect gift for loved ones.',
            'category': gold_necklaces,
            'price': Decimal('22000'),
            'image': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=800&h=800&fit=crop',
            'stock': 15
        },
        {
            'name': 'Statement Gold Collar Necklace',
            'slug': 'statement-gold-collar-necklace',
            'description': 'Bold and elegant gold collar necklace for special occasions.',
            'category': gold_necklaces,
            'price': Decimal('65000'),
            'original_price': Decimal('75000'),
            'image': 'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=800&h=800&fit=crop',
            'stock': 6
        },
        
        # Pearl Jewelry
        {
            'name': 'Classic Pearl Strand Necklace',
            'slug': 'classic-pearl-strand-necklace',
            'description': 'Timeless freshwater pearl necklace with gold clasp, perfect for any occasion.',
            'category': pearl_jewelry,
            'price': Decimal('25000'),
            'original_price': Decimal('30000'),
            'image': 'https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=800&h=800&fit=crop',
            'stock': 10,
            'is_featured': True
        },
        {
            'name': 'Pearl Drop Earrings',
            'slug': 'pearl-drop-earrings',
            'description': 'Elegant pearl drop earrings in gold setting, perfect for formal events.',
            'category': pearl_jewelry,
            'price': Decimal('18000'),
            'image': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&h=800&fit=crop',
            'stock': 20
        },
        {
            'name': 'Modern Pearl Ring',
            'slug': 'modern-pearl-ring',
            'description': 'Contemporary pearl ring design with gold band and unique setting.',
            'category': pearl_jewelry,
            'price': Decimal('12000'),
            'image': 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&h=800&fit=crop',
            'stock': 8
        },
        
        # Silver Earrings
        {
            'name': 'Sterling Silver Hoop Earrings',
            'slug': 'sterling-silver-hoop-earrings',
            'description': 'Classic sterling silver hoop earrings, versatile for any outfit.',
            'category': silver_earrings,
            'price': Decimal('5500'),
            'original_price': Decimal('7000'),
            'image': 'https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?w=800&h=800&fit=crop',
            'stock': 25,
            'is_featured': True
        },
        {
            'name': 'Crystal Silver Stud Earrings',
            'slug': 'crystal-silver-stud-earrings',
            'description': 'Sparkling crystal stud earrings in sterling silver setting.',
            'category': silver_earrings,
            'price': Decimal('8000'),
            'image': 'https://images.unsplash.com/photo-1588444837495-d6aad5922678?w=800&h=800&fit=crop',
            'stock': 18
        },
        
        # Bracelets
        {
            'name': 'Gold Tennis Bracelet',
            'slug': 'gold-tennis-bracelet',
            'description': 'Luxury gold tennis bracelet with diamonds, perfect for special occasions.',
            'category': bracelets,
            'price': Decimal('75000'),
            'original_price': Decimal('85000'),
            'image': 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&h=800&fit=crop',
            'stock': 4,
            'is_featured': True
        },
        {
            'name': 'Silver Charm Bracelet',
            'slug': 'silver-charm-bracelet',
            'description': 'Elegant silver bracelet with customizable charm options.',
            'category': bracelets,
            'price': Decimal('15000'),
            'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop',
            'stock': 12
        },
        
        # Wedding Jewelry
        {
            'name': 'Bridal Jewelry Set',
            'slug': 'bridal-jewelry-set',
            'description': 'Complete bridal set including necklace, earrings, and bracelet with diamonds.',
            'category': wedding_jewelry,
            'price': Decimal('125000'),
            'original_price': Decimal('150000'),
            'image': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=800&h=800&fit=crop',
            'stock': 3,
            'is_featured': True
        },
        {
            'name': 'Wedding Band Set',
            'slug': 'wedding-band-set',
            'description': 'Matching his and hers wedding band set in 18K gold.',
            'category': wedding_jewelry,
            'price': Decimal('35000'),
            'image': 'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&h=800&fit=crop',
            'stock': 6
        },
        
        # Men's Jewelry
        {
            'name': 'Men\'s Gold Signet Ring',
            'slug': 'mens-gold-signet-ring',
            'description': 'Classic men\'s gold signet ring with personalization options.',
            'category': mens_jewelry,
            'price': Decimal('28000'),
            'image': 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&h=800&fit=crop',
            'stock': 10
        },
        {
            'name': 'Men\'s Silver Chain',
            'slug': 'mens-silver-chain',
            'description': 'Bold sterling silver chain for men, perfect for everyday wear.',
            'category': mens_jewelry,
            'price': Decimal('12000'),
            'original_price': Decimal('15000'),
            'image': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop',
            'stock': 8
        }
    ]
    
    # Add products to database
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"   💎 Added product: {product.name}")
        else:
            print(f"   📝 Product already exists: {product.name}")

def main():
    """Main execution function"""
    print("🏪 KIRAA Jewelry Store - Product Update")
    print("=" * 50)
    
    try:
        remove_beauty_products()
        create_jewelry_categories()
        add_jewelry_products()
        
        print("\n🎉 Product update completed successfully!")
        print("📊 Current inventory:")
        print(f"   Categories: {Category.objects.count()}")
        print(f"   Products: {Product.objects.count()}")
        print(f"   Featured Products: {Product.objects.filter(is_featured=True).count()}")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    main()