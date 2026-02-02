// ================================
// Main JavaScript for KIRAA Store
// ================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('KIRAA Premium Jewelry Store loaded successfully');
    
    // Initialize all features
    initializeCartButtons();
    initializeWishlistButtons();
    initializeInteractiveBackground();
    initializeScrollAnimations();
});

/**
 * Initialize Interactive Background with Particles
 */
function initializeInteractiveBackground() {
    // Create particle container
    const particleContainer = document.createElement('div');
    particleContainer.id = 'particle-container';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    `;
    document.body.insertBefore(particleContainer, document.body.firstChild);
    
    // Create floating particles
    const particleCount = 20;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: rgba(212, 175, 55, ${Math.random() * 0.5 + 0.1});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float ${Math.random() * 20 + 15}s linear infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
        particleContainer.appendChild(particle);
    }
    
    // Track mouse movement for interactive effect
    document.addEventListener('mousemove', (e) => {
        const particles = particleContainer.querySelectorAll('div');
        particles.forEach(particle => {
            const rect = particle.getBoundingClientRect();
            const distance = Math.hypot(e.clientX - rect.left, e.clientY - rect.top);
            
            if (distance < 100) {
                particle.style.opacity = '0.8';
                particle.style.boxShadow = `0 0 10px rgba(212, 175, 55, 0.6)`;
            } else {
                particle.style.opacity = `${Math.random() * 0.5 + 0.1}`;
                particle.style.boxShadow = 'none';
            }
        });
    });
}

/**
 * Initialize Scroll Animations
 */
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all elements that should animate on scroll
    document.querySelectorAll('.product-card, .category-card, .section-title, .contact-info-card, .btn, .form-group').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Initialize Add to Cart Buttons
 */
function initializeCartButtons() {
    const cartForms = document.querySelectorAll('form[action*="add_to_cart"]');
    
    cartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Allow default submission for now
            // Could be enhanced with AJAX for better UX
        });
    });
}

/**
 * Initialize Wishlist Buttons
 */
function initializeWishlistButtons() {
    const wishlistButtons = document.querySelectorAll('.product-wishlist');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // Wishlist functionality is handled via onclick in templates
        });
    });
}

/**
 * Toggle Wishlist via AJAX
 */
function toggleWishlist(productId) {
    fetch(`/wishlist/toggle/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating wishlist', 'danger');
    });
}

/**
 * Show Notification Toast
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        ${message}
    `;
    notification.style.position = 'fixed';
    notification.style.top = '100px';
    notification.style.right = '20px';
    notification.style.zIndex = '10000';
    notification.style.maxWidth = '400px';
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

/**
 * Get CSRF Token
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Format Price
 */
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

/**
 * Update Cart Total (AJAX)
 */
function updateCart(itemId, quantity) {
    const form = new FormData();
    form.append('quantity', quantity);
    
    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        body: form,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI
            const cartTotal = document.querySelector('[data-cart-total]');
            if (cartTotal) {
                cartTotal.textContent = formatPrice(data.cart_total);
            }
            showNotification('Cart updated', 'success');
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Remove from Cart
 */
function removeFromCart(itemId) {
    if (confirm('Remove this item from cart?')) {
        fetch(`/cart/remove/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

/**
 * Change Product Image
 */
function changeImage(src) {
    const mainImage = document.getElementById('main-image');
    if (mainImage) {
        mainImage.src = src;
    }
}
