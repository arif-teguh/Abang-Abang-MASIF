from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/edit/', views.user_edit_profile, name='user_edit_profile'),
]
