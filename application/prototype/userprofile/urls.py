from django.urls import path
from . import views
from prototype.views import logout_view

urlpatterns = [
    path('', views.userprofile, name='userprofile'),
    path('logout/', logout_view, name='logout') 
]