from django.urls import include, path
from prossyApp import views
from prossyApp.views import about, add_to_cart, add_to_wishlist, ajax_add_review, ajax_contact_form, cart_view, category_list_view, category_product_list_view, checkout_view, contact, customer_dashboard, delete_item_from_cart, filter_product, index, make_address_default, order_detail, payment_completed_view, payment_failed_view, product_detail_view, product_list_view, remove_wishlist, search_view, tag_list, update_cart, wishlist_view

app_name = 'prossyApp'

urlpatterns = [
    
    #homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),
    
    #about page
    path("about/", about, name="about"),
    
    #contact page
    path("contact/", contact, name="contact"),
    
    # ajax contact page
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),

    
    #category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>", category_product_list_view, name="category-product-list"),
    
    #tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),
    
    #reviews
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),
    
    #search
    path("search/", search_view, name="search"),
    
    #filter products
    path("filter-products/", filter_product, name="filter-product"),
    
    #add to cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    
    #cart page url
    path("cart/", cart_view, name="cart"),

    #deleting from cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    #updating cart
    path("update-cart/", update_cart, name="update-cart"),
    
     #updating cart
    path("checkout/", checkout_view, name="checkout"),
    
    #Paypal payment
    path("paypal/", include("paypal.standard.ipn.urls")),
    
    #payment completed
    path("payment-completed/", payment_completed_view, name="payment-completed"),

    #payment failed
    path("payment-failed/", payment_failed_view, name="payment-failed"),
    
    #customer dashboard
    path("dashboard/", customer_dashboard, name="dashboard"),

    #order detail dashboard
    path("dashboard/order/<int:id>", order_detail, name="order-detail"),
    

   #order detail dashboard
    path("make-default-address/", make_address_default, name="make-default-address"),
      
    #wishlist
    path("wishlist/", wishlist_view, name="wishlist"),

    #add to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),
    
    #delete from wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),   
    
    
    
    
    
    
]