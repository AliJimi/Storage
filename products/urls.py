from django.urls import path
from products.views import product_list, product_create, product_detail, product_update, product_delete

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<int:pk>/', product_detail, name='product_detail'),
    path('<int:pk>/edit/', product_update, name='product_update'),
    path('<int:pk>/delete/', product_delete, name='product_delete'),
]