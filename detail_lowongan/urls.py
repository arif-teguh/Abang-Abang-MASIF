from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:id_lowongan>', views.detail_lowongan),
]
