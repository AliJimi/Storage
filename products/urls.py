from django.urls import path
from products.views import product_list, product_create, product_detail, product_update, product_delete


app_name = "products"

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<uuid:product_id>/', product_detail, name='product_detail'),
    path('<uuid:product_id>/edit/', product_update, name='product_update'),
    path('<uuid:product_id>/delete/', product_delete, name='product_delete'),
]