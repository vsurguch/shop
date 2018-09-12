from django.urls import path
from django.conf.urls import url
import basketapp.views as basketappv

app_name = 'basket'

urlpatterns = [
    path('', basketappv.basket, name='basket_index'),
    path('add/<int:id>', basketappv.basket_add1, name='basket_add'),
    path('edit/<int:id>/<int:quantity>/', basketappv.basket_edit),
    path('remove/<int:id>/', basketappv.basket_remove),
    path('basket_menu_update/', basketappv.basket_menu_update),
    # url(r'^$', basketappv.basket, name='basketindex')
]