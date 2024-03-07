from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('api/yelp/', views.yelp_proxy, name='yelp_proxy'),
]
