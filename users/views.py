from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import (
    UserRegistrationForm, UserLoginForm, 
    UserProfileForm, UserExtendedProfileForm,
    CustomPasswordChangeForm
)
from store.models import UserProfile


# ===========================
# USER REGISTRATION
# ===========================
def register(request):
    """User registration page - Creates new user accounts."""
    
    # Check if someone submitted the registration form
    if request.method == 'POST':
        # Get the form data that user filled out
        form = UserRegistrationForm(request.POST)
        
        # Check if all form fields are valid
        if form.is_valid():
            # Create the new user account
            user = form.save()
            
            # Send welcome email to new user
            send_welcome_email_to_user(user, request)
            
            # Show success message and redirect to login page
            messages.success(request, 'Account created successfully! Welcome email sent. Please log in.')
            return redirect('login')
        else:
            # If form has errors, show them to user
            show_form_errors(request, form)
    else:
        # If user just visiting page (not submitting form), show empty form
        form = UserRegistrationForm()
    
    # Prepare data to send to template
    context = {
        'form': form,
        'page_title': 'Register - Jewelry Store',
    }
    return render(request, 'users/register.html', context)


# Helper function to send welcome email
def send_welcome_email_to_user(user, request):
    """Send welcome email to newly registered user."""
    try:
        # Email subject
        email_subject = 'Welcome to KIRAA!'
        
        # Create HTML email content from template
        html_email_content = render_to_string('emails/welcome_email.html', {
            'user': user,
        })
        
        # Create plain text version (no HTML)
        plain_email_content = strip_tags(html_email_content)
        
        # Send the email
        send_mail(
            email_subject,
            plain_email_content,
            settings.DEFAULT_FROM_EMAIL,  # From email
            [user.email],  # To email
            html_message=html_email_content,
            fail_silently=False,
        )
    except Exception as email_error:
        # If email fails, still show success message but add warning
        messages.warning(request, 'Welcome email could not be sent.')


# Helper function to show form errors
def show_form_errors(request, form):
    """Display form validation errors to user."""
    for field_name, error_list in form.errors.items():
        for error_message in error_list:
            messages.error(request, f'{field_name}: {error_message}')


# ===========================
# USER LOGIN
# ===========================
def login_view(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username first
            user = authenticate(request, username=username, password=password)
            
            # If not found, try with email
            if not user:
                try:
                    user_by_email = User.objects.get(email=username)
                    user = authenticate(request, username=user_by_email.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Redirect to next page or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login - Jewelry Store',
    }
    return render(request, 'users/login.html', context)


# ===========================
# USER LOGOUT
# ===========================
@login_required(login_url='login')
def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ===========================
# USER PROFILE
# ===========================
@login_required(login_url='login')
def profile(request):
    """User profile page."""
    profile_obj = request.user.profile
    
    context = {
        'profile': profile_obj,
        'page_title': 'My Profile',
    }
    return render(request, 'users/profile.html', context)


# ===========================
# EDIT PROFILE
# ===========================
@login_required(login_url='login')
def edit_profile(request):
    """Edit user profile."""
    profile_obj = request.user.profile
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = UserExtendedProfileForm(request.POST, request.FILES, instance=profile_obj)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = UserExtendedProfileForm(instance=profile_obj)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': 'Edit Profile',
    }
    return render(request, 'users/edit_profile.html', context)


# ===========================
# CHANGE PASSWORD
# ===========================
@login_required(login_url='login')
def change_password(request):
    """Change password page."""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'page_title': 'Change Password',
    }
    return render(request, 'users/change_password.html', context)


# ===========================
# DELETE ACCOUNT
# ===========================
@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_account(request):
    """Delete user account."""
    user = request.user
    username = user.username
    user.delete()
    messages.success(request, f'Account {username} has been deleted.')
    return redirect('home')

