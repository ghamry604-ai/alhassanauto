from django.urls import path
from . import views

app_name = 'dealership'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<slug:slug>/', views.car_detail, name='car_detail'),
]
