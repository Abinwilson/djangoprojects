from django.shortcuts import render, redirect
from shop.models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

def all_categories(request):
    c = Category.objects.all()
    return render(request, 'category.html', {'c': c})


def allproducts(request, p):
    c = Category.objects.get(name=p)
    p = Product.objects.filter(category=c)
    return render(request, 'product.html', {'c': c, 'p': p})


def details(request, p):
    product = Product.objects.get(name=p)
    return render(request, 'detail.html', {'p': product})


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        email = request.POST['email']
        if password == confirmpassword:
            u = User.objects.create_user(username=username, password=password, email=email)
            u.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse('Password Not Matching')
    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        name = request.POST['username']
        pass1 = request.POST['password']
        user = authenticate(username=name, password=pass1)
        if user:
            login(request, user)
            return redirect('shop:allcat')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return user_login(request)
