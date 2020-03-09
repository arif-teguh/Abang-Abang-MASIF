from django.urls import path, include
from . import views

urlpatterns = [
    path('detail-lowongan/', include('detail_lowongan.urls')),
    path('', views.cari_lowongan),
]
