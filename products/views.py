from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem
from .forms import ProductForm
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    products = Product.objects.all()
    product_name = request.GET.get('product_name')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')
    in_stock = request.GET.get('in_stock')

    filters = dict()

    if product_name:
        filters['name__icontains'] = product_name

    if min_price:
        filters['price__gt'] = float(min_price)

    if min_price:
        filters['price__lt'] = float(max_price)

    if in_stock == 'on':
        filters['stock_qty__gt'] = 0

    if category:
        filters['category'] = category

    products = Product.objects.filter(**filters)

    paginator_obj = Paginator(products, 2)
    page_number = request.GET.get('page')
    try:
            products = paginator_obj.get_page(page_number)
    except PageNotAnInteger:
            products = paginator_obj.page(1)
    except EmptyPage:
            products = paginator_obj.page(paginator_obj.num_pages)
            context = {'page_obj': products}
            return render(request, 'index.html', context)

    sort_by = request.GET.get('sort')

    if sort_by:
        products = products.order_by(sort_by)

    categories = Category.objects.all()

    return render(request, 'home.html', 
                  {'products' : products, 'categories' : categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', context={'product' : product})

def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product created successfully')

            return redirect('home')

    return render(request, 'create_product.html', context={'form' : form})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your product has been Updated successfully.')
            return redirect('product_detail', product_id=product_id)

    return render(request, 'product_form.html',
                  {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.add_message(request, messages.SUCCESS, 'Your product has been deleted.')
    return redirect('home')

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', context={'cart' : cart})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.create(product=product, 
                                        cart=request.user.cart)
    return redirect('product_detail', product_id=product_id)

def delete_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, 
                                        cart=request.user.cart)
    cart_item.delete()
    return redirect('cart')
    

