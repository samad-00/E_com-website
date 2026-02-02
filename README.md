# 💎 Luxura - Premium Jewelry E-Commerce Store

A fully functional, premium e-commerce website for jewelry built with Django, HTML5, and CSS3. Inspired by luxury brands like Tira, featuring a modern, minimal design with gold accents and elegant typography.

## 🌟 Features

### User Authentication
- ✅ User Registration with email validation
- ✅ Secure Login/Logout
- ✅ User Profile Management
- ✅ Password Change
- ✅ Profile Avatar Upload
- ✅ Address Book

### Product Management
- ✅ 15+ Premium Jewelry Products (pre-loaded)
- ✅ 5 Product Categories (Rings, Necklaces, Earrings, Bracelets, Beauty)
- ✅ Product Images with Gallery
- ✅ Product Ratings & Reviews
- ✅ Product Search & Filtering
- ✅ Category Browsing
- ✅ Price Range Filters
- ✅ Multiple Sort Options (Price, Popularity, Newest)
- ✅ Discount Display

### Shopping Cart
- ✅ Session-based cart (anonymous users)
- ✅ Database-backed cart (registered users)
- ✅ Add/Remove/Update quantity
- ✅ Real-time cart total
- ✅ Persistent cart (for logged-in users)

### Wishlist
- ✅ Save favorite products
- ✅ View wishlist
- ✅ Add wishlist items to cart
- ✅ One-click wishlist toggle

### Checkout & Orders
- ✅ Checkout form with address validation
- ✅ Order creation and confirmation
- ✅ Multiple payment methods (Cash on Delivery, Stripe Test Mode)
- ✅ Order history tracking
- ✅ Order status tracking (Pending, Confirmed, Processing, Shipped, Delivered)
- ✅ Order details page

### Admin Dashboard
- ✅ Django Admin interface
- ✅ Product management
- ✅ Category management
- ✅ Order management
- ✅ User management
- ✅ Review moderation
- ✅ Stock management

### Design & UX
- ✅ Premium, minimal design
- ✅ Gold and black color scheme with white background
- ✅ Smooth hover animations
- ✅ Responsive design (mobile + desktop)
- ✅ Large product images
- ✅ Elegant fonts (Playfair Display + Poppins)
- ✅ Spacious layout with generous padding
- ✅ Toast notifications
- ✅ Loading spinners
- ✅ Sticky navbar

## 🛠️ Tech Stack

- **Backend:** Django 6.0.1 (Python)
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3
- **Authentication:** Django built-in auth system
- **Forms:** Django Forms + django-crispy-forms
- **Images:** Pillow
- **Payment (Test):** Stripe SDK

## 📋 Project Structure

```
shop/
├── jewelry_shop/               # Project settings
│   ├── settings.py            # Django configuration
│   ├── urls.py                # Main URL router
│   └── wsgi.py                # WSGI configuration
├── store/                      # Main app (products, cart, orders)
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   ├── urls.py                # Store URLs
│   ├── forms.py               # Product forms
│   ├── admin.py               # Admin configuration
│   └── context_processors.py  # Template context
├── users/                      # User app (auth, profile)
│   ├── models.py              # User signals
│   ├── views.py               # Auth views
│   ├── urls.py                # Auth URLs
│   └── forms.py               # Auth forms
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── store/                 # Store templates
│   │   ├── home.html
│   │   ├── shop.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_confirmation.html
│   │   ├── user_orders.html
│   │   ├── wishlist.html
│   │   └── category.html
│   └── users/                 # User templates
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── edit_profile.html
│       └── change_password.html
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── main.js            # JavaScript
│   └── images/                # Product images
├── media/                      # User uploads
│   ├── products/              # Product images
│   ├── avatars/               # User avatars
│   └── categories/            # Category images
├── manage.py                   # Django management
└── db.sqlite3                  # Database

```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone/Extract the project:**
   ```bash
   cd shop
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install django pillow stripe django-crispy-forms crispy-bootstrap5
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser account:**
   ```bash
   python manage.py createsuperuser
   # Username: admin
   # Email: admin@luxura.com
   # Password: (set your password)
   ```

6. **Populate sample data (optional):**
   ```bash
   python manage.py shell < populate_data.py
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   - Store: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## 👤 Default Admin Account

- **Username:** admin
- **Email:** admin@luxura.com
- **Password:** (Set during createsuperuser)

## 🗂️ Database Models

### Category
- name (unique)
- slug (unique)
- description
- image
- created_at

### Product
- name
- slug (unique)
- description
- category (FK to Category)
- price
- original_price (for discounts)
- image, image_2, image_3 (gallery)
- stock
- is_featured
- is_new
- created_at, updated_at

### Review
- product (FK to Product)
- user (FK to User)
- rating (1-5 stars)
- comment
- created_at

### Wishlist
- user (OneToOne to User)
- products (M2M to Product)
- created_at

### CartItem
- user (FK to User)
- product (FK to Product)
- quantity
- added_at, updated_at

### Order
- user (FK to User)
- order_number (unique)
- first_name, last_name, email, phone
- address, city, state, postal_code, country
- total_price
- payment_method (COD / Stripe)
- status (Pending, Confirmed, Processing, Shipped, Delivered, Cancelled)
- created_at, updated_at
- paid (boolean)
- transaction_id

### OrderItem
- order (FK to Order)
- product (FK to Product)
- quantity
- price

### UserProfile
- user (OneToOne to User)
- phone, address, city, state, postal_code, country
- avatar
- bio
- newsletter (boolean)
- created_at, updated_at

## 🎨 Design Colors

```css
--primary-color: #d4af37       /* Soft Gold */
--dark-color: #1a1a1a          /* Nearly Black */
--light-color: #f5f5f5         /* Off White */
--white: #ffffff               /* Pure White */
--text-dark: #333333           /* Dark Text */
--text-light: #666666          /* Light Text */
--border-color: #e0e0e0        /* Borders */
```

## 📝 Features Overview

### Home Page
- Hero section with promotional banner
- Featured products section
- New arrivals
- Category showcase
- Why Choose Us section
- Newsletter signup

### Shop Page
- Product grid layout
- Sidebar filters (category, price range)
- Search functionality
- Sorting options
- Pagination
- Product cards with ratings

### Product Detail Page
- Image gallery with zoom
- Detailed product information
- Stock availability
- Add to cart with quantity
- Wishlist toggle
- Customer reviews
- Related products
- Rating display

### Cart
- Product list with images
- Quantity adjustment
- Remove items
- Real-time total calculation
- Checkout button
- Continue shopping option
- Promo code input

### Checkout
- Shipping information form
- Billing address
- Payment method selection (COD / Stripe)
- Order summary
- Security information
- Order placement

### User Authentication
- Clean registration form
- Email validation
- Login with username or email
- "Remember me" option
- Password reset link
- Social login ready

### User Profile
- Personal information display
- Address management
- Avatar upload
- Order history
- Wishlist management
- Password change
- Account statistics

## 🔒 Security Features

- ✅ CSRF protection on all forms
- ✅ Password hashing with Django auth
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ Secure session handling
- ✅ User authentication required for cart/checkout
- ✅ Order access control (users can only see their orders)

## 📱 Responsive Design

The site is fully responsive with breakpoints for:
- **Desktop:** 1200px+
- **Tablet:** 768px - 1199px
- **Mobile:** Below 768px

All product grids, forms, and navigation adapt seamlessly.

## 🎯 URL Routes

### Store URLs
```
/ → Home
/shop/ → Shop (all products)
/search/ → Search results
/category/<slug>/ → Category products
/product/<slug>/ → Product detail
/cart/ → Shopping cart
/cart/add/<id>/ → Add to cart
/cart/update/<id>/ → Update quantity
/cart/remove/<id>/ → Remove item
/checkout/ → Checkout
/order-confirmation/<id>/ → Order confirmation
/orders/ → User orders
/wishlist/ → Wishlist
/wishlist/toggle/<id>/ → Add/remove wishlist
```

### User URLs
```
/accounts/register/ → Registration
/accounts/login/ → Login
/accounts/logout/ → Logout
/accounts/profile/ → User profile
/accounts/profile/edit/ → Edit profile
/accounts/profile/change-password/ → Change password
/accounts/profile/delete/ → Delete account
```

### Admin
```
/admin/ → Django admin panel
```

## 📧 Email Configuration

Currently configured for console backend (prints to console). To use real emails, update settings.py:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 💳 Payment Integration

### Cash on Delivery
Already implemented and ready to use.

### Stripe (Test Mode)
- Update `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` in settings.py
- Use Stripe test cards for testing

## 🧪 Testing the Store

### Test Users
You can create test users via:
1. Register page: `/accounts/register/`
2. Django admin: `/admin/`

### Test Products
15 premium jewelry products are pre-loaded with sample data.

### Test Orders
1. Login to your account
2. Browse and add products to cart
3. Proceed to checkout
4. Fill in shipping details
5. Select payment method
6. Place order
7. View order confirmation and history

## 🔧 Customization

### Add New Product
1. Go to `/admin/store/product/add/`
2. Fill in product details
3. Upload images
4. Save

### Add New Category
1. Go to `/admin/store/category/add/`
2. Enter category name and details
3. Save

### Modify Colors
Edit `/static/css/style.css` and update CSS variables in `:root` section.

### Change Store Name
Search "Luxura" in templates and update to your store name.

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [Font Awesome Icons](https://fontawesome.com/)
- [Google Fonts](https://fonts.google.com/)

## 🐛 Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Database errors
```bash
python manage.py migrate
python manage.py makemigrations
```

### Port already in use
```bash
python manage.py runserver 8001
```

### Clear cache
```bash
python manage.py clear_cache
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues or questions, refer to the Django and e-commerce best practices documentation.

---

## ✨ Future Enhancements

- [ ] Stripe full integration with real payments
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Inventory management
- [ ] Bulk order discounts
- [ ] Coupon system
- [ ] Customer reviews moderation
- [ ] Multiple currencies
- [ ] Social media integration
- [ ] Marketing email campaigns
- [ ] SMS notifications
- [ ] Advanced search with autocomplete
- [ ] Video product demos
- [ ] AR try-on feature
- [ ] Live chat support

---

**Built with ❤️ by Premium E-Commerce Team**
**Last Updated: February 2026**
