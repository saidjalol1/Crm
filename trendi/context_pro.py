from main.models import  CartItems

def wishlist(request):
    try:
        cart_items = CartItems.objects.filter(session_key=session_key).select_related('product__category')
    except CartItems.DoesNotExist:
        cart_items = " "
    return {'wishlist': cart_items}