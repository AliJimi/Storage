from django.urls import path
from . import views

urlpatterns = [
    path('', views.batch_list, name='batch_list'),
    path('create/', views.batch_create, name='batch_create'),
    path('<int:pk>/', views.batch_detail, name='batch_detail'),
    path('<int:pk>/edit/', views.batch_update, name='batch_update'),
    path('<int:pk>/delete/', views.batch_delete, name='batch_delete'),
    path('product/<int:product_id>/', views.batch_list_by_product, name='batch_list_by_product'),
    path('location/<int:location_id>/', views.batch_list_by_location, name='batch_list_by_location'),
    path('expiring/', views.expiring_batches, name='expiring_batches'),
]