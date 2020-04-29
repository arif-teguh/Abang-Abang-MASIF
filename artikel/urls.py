from django.urls import path

from . import views

urlpatterns = [
    path('form/',
         views.show_form_artikel,
         name="show_form_artikel"),

    path('form/post/',
         views.post_form_artikel,
         name="post_form_artikel"),

    path('form/edit/<int:id_artikel>/',
         views.update_form_artikel,
         name="update_form_artikel"),
]
