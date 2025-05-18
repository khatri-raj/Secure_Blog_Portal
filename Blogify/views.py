from django.contrib import messages
from django.shortcuts import render, redirect
from .models import blogify
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def home(request):
    latest_blogs = blogify.objects.filter(status='published').order_by('-created_at')[:3]
    return render(request, 'home.html', {'latest_blogs': latest_blogs})

@login_required
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        content = request.POST.get('content')
        status = request.POST.get('status', 'draft')
        image = request.FILES.get('image')

        blog = blogify(
            title=title,
            author=author,
            content=content,
            status=status,
            image=image
        )
        blog.save()
        messages.success(request, 'Blog uploaded successfully!')
        return redirect('add')
    return render(request, 'add.html')

def show(request):
    blogs = blogify.objects.all().order_by('-created_at')
    return render(request, 'show.html', {'blogs': blogs})

@login_required
def edit(request, id):
    blog = blogify.objects.get(id=id)
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.author = request.POST.get('author')
        blog.content = request.POST.get('content')
        blog.status = request.POST.get('status')
        if request.FILES.get('image'):
            blog.image = request.FILES.get('image')
        blog.save()
        messages.success(request, 'Blog updated successfully!')
        return redirect('show')
    return render(request, 'edit.html', {'blog': blog})

@login_required
def delete(request, id):
    blog = blogify.objects.get(id=id)
    blog.delete()
    messages.success(request, 'Blog deleted successfully!')
    return redirect('show')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! You can now login.")
        return redirect('login')

    return render(request, 'register.html')

def help(request):
    return render(request,'help.html')