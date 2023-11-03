from django.urls import path
from prossyApp import views
from prossyApp.views import category_list_view, category_product_list_view, index, product_detail_view, product_list_view, tag_list

app_name = 'prossyApp'

urlpatterns = [
    
    #homepage
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("product/<pid>/", product_detail_view, name="product-detail"),

    
    #category
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>", category_product_list_view, name="category-product-list"),
    
    #tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags")
    


]