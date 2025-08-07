from django.urls import path
from . import views, auth_views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.user_login, name='login'),
    path('register/', auth_views.user_register, name='register'),
    path('logout/', auth_views.user_logout, name='logout'),
    
    # Main application URLs
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('api/product-stock/<int:product_id>/', views.get_product_stock, name='get_product_stock'),
]
