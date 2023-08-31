from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def HomePage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_profile = UserProfile.objects.get(email=email)
                if user_profile.password == password:
                    # Password matches, log in the user
                    request.session['user_id'] = user_profile.id
                    return redirect('admin_dashboard')  # Make sure this name matches the one in urls.py
                else:
                    # Handle invalid password and display an error message
                    messages.error(request, 'Invalid email or password.')
            except UserProfile.DoesNotExist:
                # Handle user not found and display an error message
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})

def SignupPage(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                form.add_error('confirm_password', 'Passwords do not match.')
            else:
                form.save()
                return redirect('home')  # Redirect to a success page or any other page
    else:
        form = UserProfileForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def AdminDashboard(request):
    return render(request, 'admin.html')

def logout_user(request):
    logout(request)
    return redirect('home')  # Redirect to the login page (name='home' as per your urls.py)

