from django.http import HttpResponse
from django.shortcuts import render

from prossyApp.models import Product, Category, CartOrder, CartOrderItems, ProductImages, ProductReview, Address, Wishlist


def index(request):
    # products = Product.objects.all()
    
    products = Product.objects.filter(product_status="published", featured=True)
    
    context = {
        "products": products
    }
    
    return render(request, 'core/index.html', context)