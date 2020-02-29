from django.contrib.auth.views import LoginView
from django.urls import path

from admin.admin_login_form import AdminAuthenticationForm
from . import views

urlpatterns = [
    path('', views.admin_index, name='admin'),
    path('login/', LoginView.as_view(template_name='admin/admin_login.html',
                                     form_class=AdminAuthenticationForm,
                                     ),
         name='admin_login'),
]
