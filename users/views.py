from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

def register_view(request):

    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.add_message(request, messages.SUCCESS, f'User for {username} has been created successfully')

            return redirect('home')
        
    return render(request, 'user_form.html', {'form' : form})

def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f'User {username} logged in')
            return redirect('home')
        messages.add_message(request, messages.WARNING, f'Wrong credentials')

    return render(request, 'user_form.html', {'form' : form})

def logout_view(request):
    logout(request)

    return redirect('home')


