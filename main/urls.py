from django.urls import path
from .views import OrdersView,OrderDetail, OrdersStatusView, StorageView, ExpensesView, StaffsView, PackageView,PackageDetailView

app_name = 'main'
urlpatterns = [
    path('orders/', OrdersView.as_view(), name='order_page'),
    path('orders/orders_status', OrdersStatusView.as_view(), name='orders_status'),
    path('orders/<pk>', OrderDetail.as_view(), name='order_detail'),
    path('storage/', StorageView.as_view(), name='storage'),
    path('expenses/',ExpensesView.as_view(), name='expenses'),
    path('staffs/',StaffsView.as_view(), name='staffs'),
    path('naborlar/',PackageView.as_view(), name='package_add'),
    path('naborlar/detail/<pk>', PackageDetailView.as_view(),name='package_detail')
]