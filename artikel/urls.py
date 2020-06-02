from django.urls import path

from . import views

urlpatterns = [
    path(
        '<int:artikel_id>/',
        views.view_read_artikel,
        name='view_read_artikel'
    ),
    path('form/',
         views.show_form_artikel,
         name="show_form_artikel"),

    path('form/post/',
         views.post_form_artikel,
         name="post_form_artikel"),

    path('form/edit/<int:id_artikel>/',
         views.update_form_artikel,
         name="update_form_artikel"),

    path('form/edit/<int:id_artikel>/delete/',
         views.admin_delete_artikel,
         name="delete_artikel"),
]
