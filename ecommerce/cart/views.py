from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart, Account, Order


# Create your views here.

def cart_view(request):
    total = 0
    u = request.user
    try:
        cart = Cart.objects.filter(user=u)
        for i in cart:
            total += i.quantity * i.product.price
    except:
        pass

    return render(request, 'cart.html', {'c': cart, 'total': total})


@login_required
def add_to_cart(request, p):
    product = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=product)
        if cart.quantity < cart.product.stock:
            cart.quantity += 1
            cart.save()
    except:
        cart = Cart.objects.create(product=product, user=u, quantity=1)
        cart.save()
    return redirect('cart:cart_view')


def cart_remove(request, p):
    product = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=product)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return redirect('cart:cart_view')


def full_remove(request, p):
    product = Product.objects.get(name=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=product)
        cart.delete()
    except:
        pass
    return redirect('cart:cart_view')


def order_form(request):
    if request.method == "POST":
        address = request.POST['address']
        phone = request.POST['phone']
        accountnumber = request.POST['accountnumber']
        u = request.user
        cart = Cart.objects.filter(user=u)

        # total amount
        total = 0
        for i in cart:
            total += i.quantity * i.product.price

        # check whether user has sufficient amount in his/her account.
        ac = Account.objects.get(account_number=accountnumber)
        if ac.amount >= total:
            ac.amount = ac.amount - total
            ac.save()

            for i in cart:  # creates record in order table for each object in cart table for the current user
                o = Order.objects.create(user=u, product=i.product, address=address, phone=phone,
                                         no_of_items=i.quantity, order_status="paid")
                o.save()
                i.product.stock = i.product.stock - i.quantity
                i.product.save()
            cart.delete()  # clears the cart items for the current user
            msg = "Order Placed Successfully"
            return render(request, 'orderdetail.html', {'m': msg})
        else:
            msg = "Insufficient Amount in User Account.You cannot place order."
            return render(request, 'orderdetail.html', {'m': msg})
    return render(request, 'orderform.html')


def order_view(request):
    u = request.user
    o = Order.objects.filter(user=u)
    return render(request, 'orderview.html', {'o': o, 'u': u})
