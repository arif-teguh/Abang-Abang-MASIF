from django.urls import path

from . import views

urlpatterns = [
    path('', views.account_redirector, name='account_redirector'),
]
