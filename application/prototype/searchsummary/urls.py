from django.urls import path
from . import views
from prototype.views import logout_view

urlpatterns = [
    path('', views.search_summary, name='search_summary'),
    path('searchsummary/', views.search_summary, name='searchsummary'),
    path('logout/', logout_view, name='logout')
]
