from django.contrib.auth.views import LoginView
from django.urls import path

from opd.opd_login_form import OpdAuthenticationForm

from . import views

urlpatterns = [
    path('', views.opd_lowongan, name='opd_lowongan'),
    path('proses-<str:id_user>-<str:id_lowongan>/<str:status>/<str:catatan>/' , views.opd_update_lamaran , name = 'opd_update_lamaran'),
    path('lowongan/file_tambahan-<str:id_user>-<str:id_lowongan>/' , views.opd_download_file , name = 'opd_download_file'),
    path('lowongan/cv_pendaftar-<str:id_user>-<str:id_lowongan>/' , views.opd_download_cv , name = 'opd_download_cv'),
    path('lowongan/list-pendaftar-<str:id_lowongan>/', views.opd_list_pendaftar, name='opd_list_pendaftar'),
    path('lowongan/detail-<str:id_lowongan>/', views.opd_detail_lowongan, name='opd_detail_lowongan'),
    path('login/', LoginView.as_view(template_name='opd_login.html',form_class=OpdAuthenticationForm,),name='opd_login'),
    path('verification/404', views.opd_verification_not_found,
         name='opd_verification_not_found'),
    path('verification/<str:token>',
         views.opd_verification, name='opd_verification'),
    path('verification/',
         views.opd_verification_redirect, name='opd_verification_redirect'),
     
]
