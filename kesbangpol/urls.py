from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.kesbangpol_login,
         name='kesbangpol_login'),
    path('', views.kesbangpol_dashboard,
         name='kesbangpol_dashboard'),
    path('lamaran/<int:user_lamar_id>/', views.get_user_lamaran_detail,
          name='detail_lamaran')
]
