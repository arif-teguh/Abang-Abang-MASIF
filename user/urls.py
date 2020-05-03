from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views
from .user_login_form import UserAuthenticationForm

urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/edit/', views.user_edit_profile, name='user_edit_profile'),
    path('dashboard/edit/upload_cv/', views.upload_cv, name='user_edit_upload_cv'),
    path('dashboard/edit/upload_profile_picture/', views.upload_profile_picture, name='user_edit_upload_pp'),
    path('dashboard/edit/delete_cv/', views.delete_cv, name='delete_cv'),
    path('dashboard/api/get-all-lamaran-for-dashboard-table/', views.get_all_lamaran_for_dashboard_table,
         name='get_all_lamaran_for_dashboard_table'),
    path('register/', views.user_register, name='user_register'),
    path('register-google/', views.user_register2_google, name='user_register2_google'),
    path(
        'login/',
        LoginView.as_view(
            template_name='user_login.html',
            form_class=UserAuthenticationForm, ),
        name='user_login'),
    path('verification/404', views.user_verification_not_found,
         name="user_verification_not_found"),
    path('verification/<str:token>', views.user_verification,
         name="user_verification"),
    path('verification/', views.user_verification_redirect,
         name="user_verification_redirect"),
    path('auth/', include('social_django.urls', namespace='social')),
    path('dashboard/status-lamaran/<int:id_user_lamar_magang>/', views.user_see_status_lamaran,
         name='user_see_status_lamaran'),
]
