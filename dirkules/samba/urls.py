from django.urls import path

from . import views

app_name = 'samba'

urlpatterns = [
    path('', views.index, name='index'),
    path('config', views.config, name='config'),
    path('add', views.add, name='add'),
]