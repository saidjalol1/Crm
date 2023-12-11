from django.urls import path
from .views import *
app_name = 'trendi'

urlpatterns = [
    path('', TrendiView.as_view(), name='trendi_main'),
    path('cart_page/', CardView.as_view(), name='cart'),
    path('mywishlist/', WishListView.as_view(), name='wishlist'),
    path('add-to-wishlist/<product_id>/', add_to_wishlist, name='wishlist_add_function'),
    path('add_to_card/<product_id>', add_to_card, name='add_to_cart')
]
