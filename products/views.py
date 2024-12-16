from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm
from django.contrib import messages


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

    sort_by = request.GET.get('sort')

    if sort_by:
        products = products.order_by(sort_by)

    categories = Category.objects.all()

    return render(request, 'home.html', {'products' : products, 'categories' : categories})

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

