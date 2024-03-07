from django.urls import path
from . import views
from prototype.views import logout_view

urlpatterns = [
    path('', views.render_search_history, name='render_search_history'),
    path('logout/', logout_view, name='logout')
]
