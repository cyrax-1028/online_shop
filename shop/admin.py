from django.contrib import admin

from shop.models import Product, Category, Order, Comment

# Register your models here.


# admin.site.register(Product)
# admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Comment)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')