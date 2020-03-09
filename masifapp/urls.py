"""masifapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path, include

urlpatterns = [
    path('opd/', include('opd.urls')),
    path('admin/', include('admin.urls')),
    path('opd/', include('opd.urls')),
    path('', include('hello.urls')),
    path('account-redirector', include('account_redirector.urls')),
    path('superuser/', admin.site.urls),
    # path('auth/', include('social_django.urls')),
    # TESTING PATH dibawah ini
    path('test/', include('google_oauth2.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
         name='logout'),
]
