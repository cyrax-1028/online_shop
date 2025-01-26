from typing import Optional
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from shop.models import Product, Category, Order, Comment
from shop.forms import OrderForm, CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from shop.forms import OrderForm, ProductModelForm

# Create your views here.


def index(request, category_id: Optional[int] = None):
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product_id = pk)

    return render(request, 'shop/detail.html', {'product': product, 'comments': comments})


def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = OrderForm(request.GET)
        if form.is_valid():
            full_name = request.GET.get('full_name')
            phone_number = request.GET.get('phone_number')
            quantity = int(request.GET.get('quantity'))
            if product.quantity >= quantity:
                product.quantity -= quantity
                order = Order.objects.create(
                    full_name=full_name,
                    phone_number=phone_number,
                    quantity=quantity,
                    product=product
                )
                order.save()
                product.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Order successful sent'

                )

            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Something with wrong...'
                )


    else:
        form = OrderForm()
    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context)

def comment_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = CommentForm(request.GET)
        if form.is_valid():
            full_name = request.GET.get('full_name')
            email = request.GET.get('email')
            comment = request.GET.get('comment')
            comment = Comment.objects.create(
                full_name=full_name,
                email=email,
                comment=comment,
                product=product
            )
            comment.save()
    else:
        form = CommentForm()

    comments = Comment.objects.filter(product_id = pk)
    context = {
        'form': form,
        'product': product,
        'comments': comments
    }
    return render(request, 'shop/detail.html', context)

@login_required
def product_create(request):
    # form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductModelForm()
    context = {
        'form': form,
        'action': 'Create New'
    }
    return render(request, 'shop/create.html', context=context)


def product_delete(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return redirect('products')
    except Product.DoesNotExist as e:
        print(e)

def product_edit(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk)
    context = {
        'form': form,
        'product': product,
        'action': 'Edit'
    }
    return render(request, 'shop/create.html', context=context)