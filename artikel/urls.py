from django.urls import path

from . import views

urlpatterns = [
    path('<int:artikel_id>/', views.view_read_artikel, name='view_read_artikel'),
]
