
from django.urls import path
import adminapp.views as adminappv

app_name = 'admin'

urlpatterns = [
    path('', adminappv.main, name='main'),
    path('categories/', adminappv.categories, name='categories'),
    path('categories/create/', adminappv.create_category, name='create_category'),
    path('categories/edit/<int:id>', adminappv.edit_category, name='edit_category'),
    path('categories/delete/', adminappv.delete_category, name='delete_category'),
    path('authors/', adminappv.authors, name='authors'),
    path('authors/create/', adminappv.create_author, name='create_author'),
    path('authors/edit/<int:id>', adminappv.edit_author, name='edit_author'),
    path('authors/delete/', adminappv.delete_author, name='delete_author'),
    path('items/', adminappv.items, name='items'),
    path('items/create/', adminappv.create_item, name='create_item'),
    path('items/edit/<int:id>', adminappv.edit_item, name='edit_item'),
    path('items/delete/', adminappv.delete_item, name='delete_item'),
]