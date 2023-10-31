from django.urls import path
from prossyApp import views
from prossyApp.views import category_list_view, category_product_list_view, index, product_list_view

app_name = 'prossyApp'

urlpatterns = [
    path("", index, name="index"),
    path("products/", product_list_view, name="product-list"),
    path("category/", category_list_view, name="category-list"),
    path("category/<cid>", category_product_list_view, name="category-product-list"),


]