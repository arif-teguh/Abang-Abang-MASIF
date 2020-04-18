from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cari_lowongan),
    path('detail-lowongan/', include('detail_lowongan.urls')),
    path('sorting/waktu-magang/<str:param>', views.sort_by_waktu_magang),
    path('sorting/batas-akhir/<str:param>', views.sort_by_batas_akhir),
    path('searching/<str:param>', views.search_by_judul),
]
