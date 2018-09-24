from django.contrib import admin

from .models import Category, Author, Item
from authapp.models import MyUser, MyUserProfile
from orderapp.models import Order, OrderItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Item)
admin.site.register(MyUser)
admin.site.register(MyUserProfile)
admin.site.register(Order)
admin.site.register(OrderItem)



