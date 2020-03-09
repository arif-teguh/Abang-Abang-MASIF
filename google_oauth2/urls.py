from django.conf import settings
from django.contrib.auth import logout
from django.urls import path, include
from . import views

urlpatterns = [
    # path('google-oauth2/', include('social_django.urls', namespace='sosial')),

    path('', views.page_test)
]
