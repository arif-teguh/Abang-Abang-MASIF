from django.urls import path

from . import views

urlpatterns = [
    path('opd/form/', views.show_form_lowongan, name='form_lowongan'),
    path('opd/form/post/', views.post_form_lowongan, name='post_form_lowongan'),
    path('opd/form/edit/<int:id_lowongan>/', views.update_form_lowongan, name='update_form_lowongan'),

]
