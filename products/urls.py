from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'products'
urlpatterns = [
    path('', views.ProductsList.as_view(), name='product_list'),
    path('products/<pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('product/add_to_card/<product_id>', views.add_to_cart, name='add_to_card'),
    path('orders/', views.CustomerOrdersView.as_view(), name='customer_order_page'),
    path('orders/<pk>', views.CustomerOrderDetail.as_view(), name='cutomer_order_detail'),
    path('cart_page/', views.CardView.as_view(), name='cart'),
    path('wishlist/toggle/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.WishListView.as_view(),name='wishlist'),
    # path('product/to_card/<product_id>', views.add_to_cart, name='add_to')
    path('logout', LogoutView.as_view(), name='logout'),
]