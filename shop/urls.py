from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='ShopIndex'),
    path('about/', views.about, name='aboutUs'),
    path('contact/', views.contact, name='contactUs'),
    path('tracker/', views.tracker, name='TrackingStatus'),
    path('search/', views.search, name='Search'),
    path('product/<int:prId>', views.product, name='productView'),
    path('checkout/', views.checkout, name='Checkout'),
    path('cart/', views.cart, name='Cart'),
    path('category/<str:category>', views.category, name='Category'),

]
