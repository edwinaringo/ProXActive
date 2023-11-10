from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from taggit.models import Tag
from django.db.models import Avg
from prossyApp.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
from prossyApp.models import Product, Category, CartOrder, CartOrderItems, ProductImages, ProductReview, Address, Wishlist

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required

def index(request):
    # products = Product.objects.all()
    products = Product.objects.filter(product_status="published", featured=True, in_stock=True)

 
    context = {
        "products": products,

    }
    
    return render(request, 'core/index.html', context)

#about page
def about(request):
    return render(request, 'core/about.html')

def product_list_view(request):
    
    products = Product.objects.filter(product_status="published", in_stock=True)
    
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


def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],

        
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj'] = cart_product
        
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})
    
    
def cart_view(request):
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("prossyApp:index")
    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id, item in request.session['cart_data_obj'].items():
    #         qty = int(item['qty'])
    #         price_str = item['price']

    #         # Check if price_str is a valid numeric string
    #         if price_str.replace(".", "", 1).isdigit():
    #             price = float(price_str)
    #             cart_total_amount += qty * price

    #         return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    # else:
    #     messages.warning(request, "Your basket is empty")
    #     return redirect("prossyApp:index")


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
        
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

        
def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data
        
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

     
@login_required   
def checkout_view(request):
    
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '200',
        'item_name': 'Order-Item-No-3',
        'invoice': "INVOICE_NO-3",
        'currency_code': "USD",
        'notify_url': 'http://{}{}'.format(host, reverse("prossyApp:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("prossyApp:payment-completed")),
        'cancel_url': 'http://{}{}'.format(host, reverse("prossyApp:payment-failed")),
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
        
    return render(request, "core/checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount,'paypal_payment_button' : paypal_payment_button})


def payment_completed_view(request):
    return render(request, 'core/payment-completed.html')

def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')