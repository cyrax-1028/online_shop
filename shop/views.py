from typing import Optional
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from shop.models import Product, Category, Order, Comment
from shop.forms import OrderForm, ProductModelForm, CommentModelForm


# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        search_query = self.request.GET.get('q', '')
        filter_type = self.request.GET.get('filter', '')

        queryset = Product.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if filter_type == 'expensive':
            queryset = queryset.order_by('-price')[:5]
        elif filter_type == 'cheap':
            queryset = queryset.order_by('price')[:5]
        elif filter_type == 'rating':
            queryset = queryset.filter(rating__gte=4).order_by('-rating')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['comments'] = list(Comment.objects.filter(product=product, is_negative=False))
        context['related_products'] = Product.objects.filter(category=product.category).exclude(
            id=product.id).select_related('category')
        return context



class CreateProduct(CreateView):
    model = Product
    template_name = 'shop/create.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class DeleteProduct(DeleteView):
    model = Product
    success_url = reverse_lazy('products')


class EditProduct(UpdateView):
    model = Product
    template_name = 'shop/update.html'
    form_class = ProductModelForm

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CommentView(CreateView):
    model = Comment
    form_class = CommentModelForm
    template_name = 'shop/detail.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.product = product
        comment.save()
        return redirect('product_detail', pk=product.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        context['product'] = product
        return context


def about(request):
    return render(request, 'shop/about.html')


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shop/detail.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        quantity = form.cleaned_data['quantity']

        if product.quantity >= quantity:
            product.quantity -= quantity
            product.save()

            order = form.save(commit=False)
            order.product = product
            order.save()

            messages.success(self.request, "Order successfully sent!")
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(self.request, "Not enough stock available.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, pk=self.kwargs['pk'])
        return context
