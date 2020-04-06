from django.urls import path

from . import views

urlpatterns = [
    path('register', views.user_register, name='user_register'),
    path('verification/404', views.user_verification_not_found,
         name="user_verification_not_found"),
    path('verification/<str:token>', views.user_verification,
         name="user_verification"),
    path('verification/', views.user_verification_redirect,
         name="user_verification_redirect"),
]
