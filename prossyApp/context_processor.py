
from prossyApp.models import Product, Category, CartOrder, CartOrderItems, ProductImages, ProductReview, Address, Wishlist

def default(request):
    categories = Category.objects.all()
    address = Address.objects.get(user=request.user)
    
    return {
        'categories': categories,
        'address':address,
    }