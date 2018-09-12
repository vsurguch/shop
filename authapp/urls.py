
from django.conf.urls import url
from django.urls import path
import authapp.views as authappv

app_name = 'auth'

urlpatterns = [
    url(r'^login/$', authappv.login, name='login'),
    url(r'^logout/$', authappv.logout, name='logout'),
    url(r'^register/$', authappv.register, name='register'),
    url(r'^edit/$', authappv.edit, name='edit'),
    path('verify/<str:email>/<str:key>/', authappv.verify, name='verify')
]