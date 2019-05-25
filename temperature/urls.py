from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_current_temp, name='get_current_temp'),
    path('start/', views.start, name='start'),
]
