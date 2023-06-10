from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_entries', views.new_entries, name='new_entries'),
    path('green_list', views.green_list, name='green_list'),
]