from django.urls import path

from . import views

urlpatterns = [
    path('verification/404', views.opd_verification_not_found,
         name='opd_verification_not_found'),
    path('verification/<str:token>',
         views.opd_verification, name='opd_verification'),
    path('verification/',
         views.opd_verification_redirect, name='opd_verification_redirect'),
]
