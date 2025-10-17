from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .forms import SignupForm, LoginForm 

User = get_user_model() 

# Define constants for clean redirection
SUCCESS_REDIRECT_URL_NAME = 'home'
LOGIN_REDIRECT_URL_NAME = 'login'

def signup_view(request):
    """Handles the user registration process."""
    if request.user.is_authenticated:
        # Redirect to home if already logged in
        return redirect(SUCCESS_REDIRECT_URL_NAME) 

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                # Save user and hash password
                user = form.save() 
                login(request, user) 
                messages.success(request, f"Welcome, {user.full_name.split(' ')[0]}! Your account is created.")
                return redirect(SUCCESS_REDIRECT_URL_NAME) 
            except Exception as e:
                print(f"User creation failed: {e}")
                messages.error(request, "A database error occurred during sign up.")
            return render(request, 'signup.html', {'form': form, "success":False})

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form, "success":True})


def login_view(request):
    """
    Handles the user login process. 
    If unauthenticated, it renders 'login.html' (the correct form).
    """
    if request.user.is_authenticated:
        # If already authenticated, redirect to the home page immediately
        return redirect(SUCCESS_REDIRECT_URL_NAME)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            messages.success(request, "Login successful!")
            return redirect(SUCCESS_REDIRECT_URL_NAME)
        else:
            messages.error(request, "Invalid information. Please try again.")
            
    form = LoginForm()
    # CRITICAL: This is the line that renders the login form when not logged in.
    return render(request, 'login.html', {'form': form}) 


def logout_view(request):
    """
    Logs the user out cleanly and redirects them to the login page.
    This is the best way to clear a phantom session.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been successfully logged out.")
    return redirect(LOGIN_REDIRECT_URL_NAME)


@login_required
def home_view(request):
    """Authenticated user's home page. FIXED to render home.html."""
    # Renders the home template if the user is authenticated (enforced by @login_required)
    return render(request, 'index.html')
