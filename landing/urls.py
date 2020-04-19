from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('logout/', views.landing_logout, name="logout")
]
