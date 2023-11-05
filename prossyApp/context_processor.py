
from prossyApp.models import Category, Address, Product
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    # tags = Product.objects.filter(tags=tags)
    
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    
    return {
        'categories': categories,
        'address':address,
        # 'tags':tags,
        'min_max_price':min_max_price,

    }