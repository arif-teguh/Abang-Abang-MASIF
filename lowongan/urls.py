from django.urls import path

from . import views

urlpatterns = [
    path('opd/form/',
         views.show_form_lowongan,
         name='form_lowongan'),

    path('opd/form/post/',
         views.post_form_lowongan,
         name='post_form_lowongan'),

    path('opd/form/edit/<int:id_lowongan>/',
         views.update_form_lowongan,
         name='update_form_lowongan'),

    path('user/lamar/<int:id_lowongan>/',
         views.form_lamar_lowongan,
         name='form_lamar_lowongan'),

    path('admin/edit-kategori/',
         views.edit_pilihan_kategori_lowongan,
         name='edit_pilihan_kategori_lowongan'),

    path('admin/form/edit-kategori/',
         views.show_edit_kategori_lowongan,
         name='show_edit_kategori_lowongan'),

]
