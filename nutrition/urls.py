from django.urls import path
from . import views

urlpatterns = [
    path('', views.nutrition_list, name='nutrition_list'),
    path('create/', views.nutrition_create, name='nutrition_create'),
    path('<int:pk>/', views.nutrition_detail, name='nutrition_detail'),
    path('<int:pk>/edit/', views.nutrition_update, name='nutrition_update'),
    path('<int:pk>/delete/', views.nutrition_delete, name='nutrition_delete'),
    path('product/<int:product_id>/', views.nutrition_by_product, name='nutrition_by_product'),
]