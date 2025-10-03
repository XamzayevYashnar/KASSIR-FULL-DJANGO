from django.urls import path
from . import views

urlpatterns = [
    path('', views.barcode_list, name='barcode_list'),
    path('kassa/', views.kassa, name='kassa'),
    path('delete-barcode/<int:barcode_id>/', views.delete_barcode, name='delete_barcode'),
    path('toggle-status/<int:barcode_id>/', views.toggle_barcode_status, name='toggle_barcode_status'),
    path('stats/', views.get_stats, name='get_stats'),
]