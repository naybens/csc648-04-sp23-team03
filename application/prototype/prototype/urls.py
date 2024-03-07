"""prototype URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from .views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('signup/', include('signup.urls')),
    path('preferences/', include('preferences.urls')),
    path('searchsummary/', include('searchsummary.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('searchhistory/', include('searchhistory.urls')),
]
