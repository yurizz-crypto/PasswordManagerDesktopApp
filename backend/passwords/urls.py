from django.urls import path
from . import views

urlpatterns = [
    path('', views.password_list, name='password_list'),
    path('<int:pk>/', views.password_detail, name='password_detail'),
]