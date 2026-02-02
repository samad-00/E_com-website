# 🎉 Quick Start Guide - Jewelry Store

## 📦 Installation & Setup

### 1. Prerequisites
- Python 3.11+ installed
- Git installed
- ~500MB disk space

### 2. Clone/Extract Project
```bash
cd /path/to/shop
```

### 3. Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Database
```bash
python manage.py migrate
```

### 6. Create Admin Account
```bash
python manage.py createsuperuser
# Follow prompts to create username/password
# Example:
# Username: admin
# Email: admin@example.com
# Password: (choose a strong password)
```

### 7. Load Sample Data
```bash
python manage.py shell < populate_data.py
# Or:
python populate_data.py
```

### 8. Run Development Server
```bash
python manage.py runserver
# Server starts at http://localhost:8000/
```

---

## 🌐 Accessing Your Store

**Home Page:** http://localhost:8000/
**Admin Dashboard:** http://localhost:8000/admin/
**User Login:** http://localhost:8000/users/login/
**User Register:** http://localhost:8000/users/register/

---

## 📁 Project Structure

```
jewelry_shop/
├── jewelry_shop/          # Main project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── store/                 # E-commerce app
│   ├── models.py          # 8 database models
│   ├── views.py           # 14+ view functions
│   ├── forms.py           # Forms for reviews/checkout
│   ├── urls.py            # Store URLs
│   ├── admin.py           # Admin customization
│   └── context_processors.py  # Cart context
├── users/                 # Authentication app
│   ├── models.py          # UserProfile model & signals
│   ├── views.py           # Auth views (register/login/profile)
│   ├── forms.py           # Auth forms
│   └── urls.py            # User URLs
├── templates/             # HTML templates
│   ├── base.html          # Base template with navbar/footer
│   ├── store/
│   │   ├── home.html
│   │   ├── shop.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_confirmation.html
│   │   ├── user_orders.html
│   │   ├── wishlist.html
│   │   ├── category.html
│   │   └── search.html
│   └── users/
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── edit_profile.html
│       ├── change_password.html
│       └── delete_account.html
├── static/                # Static files
│   ├── css/
│   │   └── style.css      # Premium CSS (1000+ lines)
│   └── js/
│       └── main.js        # JavaScript utilities
├── db.sqlite3             # SQLite database
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
├── README.md              # Full documentation
├── TESTING_GUIDE.md       # Testing workflows
└── DEPLOYMENT_GUIDE.md    # Deployment instructions
```

---

## 🎯 Core Features

### ✅ User Management
- Registration with validation
- Login (username or email)
- Profile management
- Password change
- Account deletion
- Avatar uploads

### ✅ Product Catalog
- 15 sample jewelry products
- 5 categories (Rings, Necklaces, Earrings, Bracelets, Beauty)
- Product images & gallery
- Stock management
- Pricing & discounts
- Featured & new arrival badges

### ✅ Shopping Experience
- Advanced product search
- Category filtering
- Price range filtering
- Multi-sort options (price, rating, newest)
- Pagination
- Product reviews (ratings 1-5 stars)

### ✅ Shopping Cart
- Add/remove items
- Update quantities
- Session persistence
- Real-time total calculation
- Cart context in all templates

### ✅ Wishlist
- Add products to favorites
- View wishlist
- Manage wishlist items
- Quick add-to-cart from wishlist

### ✅ Checkout & Orders
- Multi-step checkout form
- Address form with validation
- Payment method selection:
  - Cash on Delivery (COD)
  - Stripe (test mode configured)
- Order confirmation page
- Order history & tracking
- Order details viewing

### ✅ Admin Dashboard
- Complete product management
- Category management
- Order management with status tracking
- Customer management
- Review moderation
- Inline editing for quantities & pricing

### ✅ Design & UX
- Premium luxury design aesthetic
- Gold & dark theme (#d4af37, #1a1a1a)
- Fully responsive (mobile, tablet, desktop)
- Smooth animations & transitions
- Font Awesome icons
- Google Fonts (Playfair Display, Poppins)
- Accessibility features

---

## 🧪 Testing the Store

### Quick Test Workflow (5 minutes)
```
1. Go to http://localhost:8000/
2. Click "Sign Up"
3. Create an account (email: test@example.com)
4. Login
5. Go to Shop page
6. Add a product to cart
7. Click Cart icon
8. Proceed to checkout
9. Complete the form
10. Select "Cash on Delivery"
11. Place Order
12. View order confirmation
```

**See TESTING_GUIDE.md for comprehensive testing scenarios**

---

## 🔧 Common Tasks

### Add a New Product
```bash
python manage.py shell
>>> from store.models import Product, Category
>>> category = Category.objects.get(name='Rings')
>>> Product.objects.create(
...     name='Diamond Ring',
...     description='Beautiful diamond ring',
...     category=category,
...     price=999.99,
...     stock=10
... )
```

### Add Admin User
```bash
python manage.py createsuperuser
```

### Reset Database
```bash
# Warning: This deletes all data!
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python populate_data.py
```

### View Database Shell
```bash
python manage.py shell
>>> from store.models import Product
>>> Product.objects.all()
>>> Product.objects.count()
```

---

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
# Use different port
python manage.py runserver 8001
```

### "Static files not loading"
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### "Database locked"
```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
```

### "Import errors"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Documentation

- **README.md** - Full project documentation
- **TESTING_GUIDE.md** - Comprehensive testing guide
- **DEPLOYMENT_GUIDE.md** - Production deployment guide

---

## 🚀 Next Steps

1. **Explore the Store**
   - Browse products on http://localhost:8000/
   - Test all features mentioned above

2. **Customize for Your Needs**
   - Update product data
   - Modify design/colors
   - Add your own features

3. **Deploy to Production**
   - Follow DEPLOYMENT_GUIDE.md
   - Choose hosting platform
   - Configure domain & SSL

4. **Integrate Stripe Payments**
   - Get test API keys from stripe.com
   - Add to environment variables
   - Implement payment processing

5. **Setup Email Notifications**
   - Configure SendGrid or AWS SES
   - Enable order confirmation emails
   - Add customer communication

---

## 📞 Support

- Django Docs: https://docs.djangoproject.com/
- Django REST: https://www.django-rest-framework.org/
- Bootstrap 5: https://getbootstrap.com/docs/5.0/
- Stripe: https://stripe.com/docs
- Font Awesome: https://fontawesome.com/docs

---

## 📋 Requirements

**Python Packages:**
- Django 6.0.1
- Pillow 12.1.0
- Stripe 14.3.0
- django-crispy-forms 2.5
- crispy-bootstrap5 2025.6

**Browser Support:**
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

---

## ✨ Features at a Glance

| Feature | Status | Details |
|---------|--------|---------|
| User Authentication | ✅ | Register, login, profile management |
| Product Catalog | ✅ | 15 products, 5 categories, images |
| Search & Filter | ✅ | Full-text search, category/price filters |
| Shopping Cart | ✅ | Add, remove, update quantities |
| Wishlist | ✅ | Save favorite products |
| Reviews | ✅ | Rate products 1-5 stars |
| Checkout | ✅ | Multi-step form with validation |
| Payment | ⚙️ | COD ready, Stripe configured |
| Orders | ✅ | Tracking, history, confirmation |
| Admin Dashboard | ✅ | Full product/order management |
| Responsive Design | ✅ | Mobile, tablet, desktop optimized |
| Premium Design | ✅ | Gold theme, modern aesthetic |

---

**Your jewelry store is ready to go! 💎✨**

Start with: `python manage.py runserver`
Then visit: `http://localhost:8000/`
