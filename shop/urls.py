from django.contrib import admin
from django.urls import path

from shop import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('category-detail/<int:category_id>/', views.ProductDetail.as_view(), name='products_of_category'),
    path('create-product/', views.CreateProduct.as_view(), name='product_create'),
    path('delete-product/<int:pk>/', views.DeleteProduct.as_view() , name='product_delete'),
    path('edit-product/<int:pk>/', views.EditProduct.as_view(), name='product_edit'),
    path('order-detail/<int:pk>/save/', views.OrderCreateView.as_view(), name='order_detail'),
    path('product-comments/<int:pk>/', views.CommentView.as_view(), name='comment_view'),
    path('about/', views.about, name='about'),
]