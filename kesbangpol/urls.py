from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.kesbangpol_login,
         name='kesbangpol_login'),
    path('', views.kesbangpol_dashboard,
         name='kesbangpol_dashboard')
]
