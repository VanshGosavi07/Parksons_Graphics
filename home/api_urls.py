from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import api_views

# API Documentation Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Warehouse Inventory API",
        default_version='v1',
        description="""
        Warehouse Inventory Management System API
        
        This API provides endpoints for managing warehouse inventory including:
        - Product management (CRUD operations)
        - Stock transaction recording (IN/OUT)
        - Inventory reporting and analytics
        - Stock level monitoring
        
        ## Features:
        - Create and manage products with unique SKUs
        - Record stock movements (IN for receiving, OUT for shipping/sales)
        - Real-time inventory tracking
        - Low stock alerts
        - Comprehensive transaction history
        
        ## Validation:
        - SKU uniqueness validation
        - Stock availability validation for OUT transactions
        - Positive quantity validation
        - Required field validation
        """,
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@warehouse.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API Router
router = DefaultRouter()
router.register(r'products', api_views.ProductMasterViewSet)
router.register(r'transactions', api_views.StockMainViewSet)
router.register(r'transaction-details', api_views.StockDetailViewSet)
router.register(r'inventory', api_views.InventoryReportViewSet, basename='inventory')

urlpatterns = [
    # API Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API Endpoints
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
