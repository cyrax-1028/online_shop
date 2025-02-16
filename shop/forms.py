from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Product, Comment, Order


class OrderForm(forms.ModelForm):
    phone_number = PhoneNumberField(region='UZ')

    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'quantity']


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'content']