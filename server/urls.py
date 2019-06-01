from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reception/', views.reception, name='reception'),
    path('get_records_and_invoice/', views.get_records_and_invoice, name='get_records_and_invoice'),
    path('manager/', views.manager, name='manager'),
    path('manager_set_para/', views.manager_set_para, name='manager_set_para'),
    path('manager_check_state/', views.manager_check_state, name='manager_check_state'),
    path('boss/', views.boss, name='boss'),
    path('boss_print_report/', views.boss_print_report, name='boss_print_report'),
]
