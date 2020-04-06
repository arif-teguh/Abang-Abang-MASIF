from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/edit/', views.user_edit_profile, name='user_edit_profile'),
    path('dashboard/edit/upload_cv/', views.upload_cv, name='user_edit_upload_cv'),
    path('dashboard/edit/upload_profile_picture/', views.upload_profile_picture, name='user_edit_upload_pp'),
    path('dashboard/edit/delete_cv/', views.delete_cv, name='delete_cv'),
]
