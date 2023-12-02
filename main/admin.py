from django.contrib import admin
from .models import Orders, CartItems, OrderItems, WishList, Expenses, UserTrack, Deliver, Staffs

admin.site.register(Orders)
admin.site.register(CartItems)
admin.site.register(OrderItems)
admin.site.register(WishList)
admin.site.register(Expenses)
admin.site.register(UserTrack)
admin.site.register(Deliver)
admin.site.register(Staffs)