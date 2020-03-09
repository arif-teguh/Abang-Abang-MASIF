from django.conf import settings
from django.contrib.auth import logout
from django.urls import path, include
from . import views

urlpatterns = [
    # path('google-oauth2/', include('social_django.urls', namespace='sosial')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('', views.page_test),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
]
