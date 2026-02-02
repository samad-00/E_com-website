from django.contrib import admin
from .models import (
    Category, Product, Review, Wishlist, 
    CartItem, Order, OrderItem, UserProfile, ContactQuery
)

# ===========================
# CATEGORY ADMIN
# ===========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('created_at',)


# ===========================
# PRODUCT ADMIN
# ===========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured', 'is_new', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'is_featured', 'is_new', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_featured', 'is_new')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Media', {
            'fields': ('image', 'image_2', 'image_3')
        }),
        ('Stock & Status', {
            'fields': ('stock', 'is_featured', 'is_new')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ===========================
# REVIEW ADMIN
# ===========================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at', 'product', 'user')


# ===========================
# WISHLIST ADMIN
# ===========================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    filter_horizontal = ('products',)
    search_fields = ('user__username',)


# ===========================
# CART ITEM ADMIN
# ===========================
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('added_at', 'updated_at')


# ===========================
# ORDER ITEM INLINE
# ===========================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


# ===========================
# ORDER ADMIN
# ===========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_price', 'status', 'payment_method', 'paid', 'created_at')
    list_filter = ('status', 'payment_method', 'paid', 'created_at')
    search_fields = ('order_number', 'user__username', 'email')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'user')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'created_at', 'updated_at')
        }),
        ('Shipping Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Order Details', {
            'fields': ('total_price', 'payment_method', 'status', 'paid', 'transaction_id')
        }),
    )
    list_editable = ('status', 'paid')


# ===========================
# USER PROFILE ADMIN
# ===========================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'newsletter', 'created_at')
    list_filter = ('newsletter', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
    readonly_fields = ('created_at', 'updated_at')


# ===========================
# CONTACT QUERY ADMIN
# ===========================
@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'query_type', 'status', 'created_at')
    list_filter = ('query_type', 'status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Query Details', {
            'fields': ('query_type', 'product', 'subject', 'message')
        }),
        ('Response', {
            'fields': ('status', 'response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
