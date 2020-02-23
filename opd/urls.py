from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.opd_login, name='opd_login')
]