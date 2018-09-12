
from django.urls import path
from django.conf.urls import url

from .views import index, catalog, contacts, catalog_update

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
]