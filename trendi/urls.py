from django.urls import path
from .views import *
app_name = 'trendi'

urlpatterns = [
    path('', TrendiView.as_view(), name='trendi_main'),
    path('cart_page/', CardView.as_view(), name='cart'),
]
