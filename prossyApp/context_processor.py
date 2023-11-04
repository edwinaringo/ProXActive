
from prossyApp.models import Category, Address, Product

def default(request):
    categories = Category.objects.all()
    # tags = Product.objects.filter(tags=tags)
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    
    return {
        'categories': categories,
        'address':address,
        # 'tags':tags,
    }