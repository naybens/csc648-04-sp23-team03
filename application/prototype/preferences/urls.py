from django.urls import path
from . import views
from prototype.views import logout_view

urlpatterns = [
    path('', views.preferences, name='preferences'),
    path('search/', views.search, name='search'),
    path('logout/', logout_view, name='logout')
]
