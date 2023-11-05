from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag
from django.db.models import Avg
from prossyApp.forms import ProductReviewForm
from django.template.loader import render_to_string

from prossyApp.models import Product, Category, CartOrder, CartOrderItems, ProductImages, ProductReview, Address, Wishlist


def index(request):
    # products = Product.objects.all()
    
    products = Product.objects.filter(product_status="published", featured=True)
    
    context = {
        "products": products
    }
    
    return render(request, 'core/index.html', context)

def product_list_view(request):
    
    products = Product.objects.filter(product_status="published")
    
    context = {
        "products": products
    }
    
    return render(request, 'core/product-list.html', context)

def category_list_view(request):
    categories = Category.objects.all()
    
    context = {
        "categories": categories
    }
    
    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    
    context = {
        "category": category,
        "products": products,
    }
    
    return render (request, "core/category-product-list.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    p_image = product.p_images.all()
    
    #Reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    
    #Average Reviews
    average_rating =ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    #Comment form
    review_form = ProductReviewForm()
    
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count =ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count > 0:
            make_review = False
    
    context = {
        "p": product,
        "p_image": p_image,
        "review_form": review_form,
        "make_review": make_review,


        "products": products,
        "reviews":reviews,
        "average_rating": average_rating,

    }
    
    return render(request, "core/product-detail.html", context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        
        context = {
            "products": products
        }
        
        return render (request, "core/tag.html", context)
    
def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],

    )
    
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews,
        }
        
    )
    
def search_view(request):
    query = request.GET.get("q")
    
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    
    context = {
        "products": products,
        "query": query,
    }
    
    return render(request, "core/search.html", context)

def filter_product(request):
    categories = request.GET.getlist('category[]')
    tags = request.GET.getlist('tags[]')
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    
    products = Product.objects.filter(product_status = "published").order_by("-id").distinct()
    
    products =products.filter(price__gte=min_price)
    products =products.filter(price__lte=max_price)

    
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
        
    if len(tags) > 0:
        products = products.filter(tags__id__in=tags).distinct()
        
    data = render_to_string("core/async/product-list.html", {"products": products})
    return JsonResponse({"data": data})