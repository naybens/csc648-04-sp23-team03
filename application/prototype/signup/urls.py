from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('createuser/', views.createuser_view),
]