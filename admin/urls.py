from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_index, name='admin'),
    path('login/', views.admin_login, name='admin_login'),
]
