from django.urls import path
from prossyApp import views
from prossyApp.views import index

app_name = 'prossyApp'

urlpatterns = [
    path("", views.index)
]