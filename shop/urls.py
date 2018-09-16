"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

import mainapp.views as mainappv

urlpatterns = [
    url(r'^', include('mainapp.urls', namespace='main')),
    path('catalog/', mainappv.catalog, name='catalog'),
    path('catalog_update/', mainappv.catalog_update, name='catalog_update'),
    path('contacts/', mainappv.contacts, name='contacts'),
    path('item/<int:id>', mainappv.item_view, name="item_view"),
    # path('admin/', include('adminapp.urls', namespace='admin')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    # url('^$', mainappv.index, name='main'),
    # path('', mainappv.index),
    path('admin/', admin.site.urls),
    # url(r'^auth/', include('authapp.urls', namespace='auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
