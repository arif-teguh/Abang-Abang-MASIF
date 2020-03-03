from django.contrib.auth.views import LoginView
from django.urls import path

from opd.opd_login_form import OpdAuthenticationForm

from . import views

urlpatterns = [
    path('', views.opd_index, name='opd'),
    path('lowongan/', views.opd_lowongan, name='opd_lowongan'),
    path('login/', LoginView.as_view(template_name='opd_login.html',form_class=OpdAuthenticationForm,),name='opd_login'),
]