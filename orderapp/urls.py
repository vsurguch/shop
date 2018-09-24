
from django.urls import path
import orderapp.views as ordersappv

app_name = 'orderapp'

urlpatterns = [
    path('', ordersappv.OrderList.as_view(), name='order_list'),
    path('create/', ordersappv.OrderItemsCreate.as_view(), name='order_create'),
    path('update/<int:pk>', ordersappv.OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>', ordersappv.OrderDelete.as_view(), name='order_delete'),
    path('details/<int:pk>', ordersappv.OrderDetailView.as_view(), name='order_detail'),
    path('return_to_basket/<int:pk>', ordersappv.back_to_basket, name='back_to_basket')
]