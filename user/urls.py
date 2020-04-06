from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .user_login_form import UserAuthenticationForm

urlpatterns = [
    path('register', views.user_register, name='user_register'),
    path(
        'login/',
        LoginView.as_view(
            template_name='user_login.html',
            form_class=UserAuthenticationForm,),
        name='user_login'),
    path('verification/404', views.user_verification_not_found,
         name="user_verification_not_found"),
    path('verification/<str:token>', views.user_verification,
         name="user_verification"),
    path('verification/', views.user_verification_redirect,
         name="user_verification_redirect"),
]
