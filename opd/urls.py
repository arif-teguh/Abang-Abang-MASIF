from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.opd_home, name='opd_home'),
    path('sorting/waktu-magang/<str:param>', views.sort_by_waktu_magang),
    path('sorting/batas-akhir/<str:param>', views.sort_by_batas_akhir),
    path('searching/<str:param>', views.search_by_judul),
    path('lowongan/buka-tutup/<str:id_lowongan>/', views.opd_tutup_lowongan, name='opd_tutup_lowongan'),
    path('proses-<str:id_user>-<str:id_lowongan>/<str:status>/<str:catatan>/', views.opd_update_lamaran,
         name='opd_update_lamaran'),
    path('lowongan/file_tambahan-<str:id_user>-<str:id_lowongan>/', views.opd_download_file, name='opd_download_file'),
    path('lowongan/cv_pendaftar-<str:id_user>-<str:id_lowongan>/', views.opd_download_cv, name='opd_download_cv'),
    path('lowongan/list-pendaftar-<str:id_lowongan>/', views.opd_list_pendaftar, name='opd_list_pendaftar'),
    path('lowongan/detail-<str:id_lowongan>/', views.opd_detail_lowongan, name='opd_detail_lowongan'),
    path('verification/404', views.opd_verification_not_found,
         name='opd_verification_not_found'),
    path('verification/<str:token>',
         views.opd_verification, name='opd_verification'),
    path('verification/',
         views.opd_verification_redirect, name='opd_verification_redirect'),
    path('editprofile/<int:pk>/',
         views.opd_edit_profile_view, name='opd_edit_profile_view'),
    path('editprofile/<int:pk>/post/',
         views.opd_edit_profile_handler, name='opd_edit_profile_post'),
    path('editprofile/<int:pk>/post/upload_profile_picture/', views.upload_profile_picture_opd,
         name='opd_edit_upload_pp'),

]
