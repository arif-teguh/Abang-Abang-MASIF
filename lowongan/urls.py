from django.urls import path

from . import views

urlpatterns = [
    path('opd/form/', views.show_form_lowongan, name='form_lowongan')
]
