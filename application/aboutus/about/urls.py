from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('', views.MemberListView.as_view(), name='all'),
    path('<int:pk>/', views.MemberDetailView.as_view(), name='detail'),
]