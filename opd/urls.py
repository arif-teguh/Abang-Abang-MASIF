from django.contrib.auth.views import LoginView
from django.urls import path

from opd.opd_login_form import OpdAuthenticationForm

from . import views

urlpatterns = [
    path('', views.opd_lowongan, name='opd_lowongan'),
    path('lowongan/detail-<str:id_lowongan>/', views.opd_detail_lowongan, name='opd_detail_lowongan'),
    path('login/', LoginView.as_view(template_name='opd_login.html',form_class=OpdAuthenticationForm,),name='opd_login'),
    path('verification/404', views.opd_verification_not_found,
         name='opd_verification_not_found'),
    path('verification/<str:token>',
         views.opd_verification, name='opd_verification'),
    path('verification/',
         views.opd_verification_redirect, name='opd_verification_redirect'),
]
