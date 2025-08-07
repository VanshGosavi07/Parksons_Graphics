from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ProductMaster, StockMain, StockDetail
from .serializers import (
    ProductMasterSerializer, 
    StockMainSerializer, 
    StockDetailSerializer,
    StockTransactionCreateSerializer,
    InventoryReportSerializer
)

class ProductMasterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products in the warehouse inventory system.
    
    Provides CRUD operations for products including:
    - List all products with current stock levels
    - Create new products with validation
    - Retrieve, update, delete individual products
    - Get current stock level for a specific product
    """
    queryset = ProductMaster.objects.all()
    serializer_class = ProductMasterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sku']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'sku', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def current_stock(self, request, pk=None):
        """Get current stock level for a specific product"""
        product = self.get_object()
        return Response({
            'current_stock': product.get_current_stock(),
            'product_name': product.name,
            'sku': product.sku
        })

class StockMainViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing stock transactions.
    
    Provides operations for:
    - List all transactions with filtering
    - Create new transactions with product details
    - Retrieve transaction details
    - Filter by transaction type (IN/OUT)
    """
    queryset = StockMain.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['remarks']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StockTransactionCreateSerializer
        return StockMainSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new stock transaction with product details"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Return full transaction data
        return_serializer = StockMainSerializer(instance)
        return Response(return_serializer.data, status=status.HTTP_201_CREATED)

class StockDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing stock transaction details.
    
    Provides read-only access to individual product movements.
    """
    queryset = StockDetail.objects.all()
    serializer_class = StockDetailSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['transaction__type', 'product']
    ordering_fields = ['transaction__date']
    ordering = ['-transaction__date']

class InventoryReportViewSet(viewsets.ViewSet):
    """
    ViewSet for generating inventory reports.
    
    Provides endpoints for:
    - Complete inventory status
    - Low stock alerts
    - Out of stock items
    """
    
    @action(detail=False, methods=['get'])
    def current_inventory(self, request):
        """Get complete current inventory status"""
        products = ProductMaster.objects.all()
        inventory_data = []
        
        for product in products:
            current_stock = product.get_current_stock()
            status_text = 'Low Stock' if current_stock <= 5 else 'In Stock' if current_stock > 0 else 'Out of Stock'
            
            inventory_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'product_sku': product.sku,
                'product_description': product.description or '',
                'current_stock': current_stock,
                'status': status_text,
                'created_at': product.created_at
            })
        
        serializer = InventoryReportSerializer(inventory_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products with low stock (≤ 5 units)"""
        products = ProductMaster.objects.all()
        low_stock_products = []
        
        for product in products:
            current_stock = product.get_current_stock()
            if current_stock <= 5:
                low_stock_products.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_sku': product.sku,
                    'product_description': product.description or '',
                    'current_stock': current_stock,
                    'status': 'Low Stock' if current_stock > 0 else 'Out of Stock',
                    'created_at': product.created_at
                })
        
        serializer = InventoryReportSerializer(low_stock_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Get products that are out of stock"""
        products = ProductMaster.objects.all()
        out_of_stock_products = []
        
        for product in products:
            current_stock = product.get_current_stock()
            if current_stock <= 0:
                out_of_stock_products.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'product_sku': product.sku,
                    'product_description': product.description or '',
                    'current_stock': current_stock,
                    'status': 'Out of Stock',
                    'created_at': product.created_at
                })
        
        serializer = InventoryReportSerializer(out_of_stock_products, many=True)
        return Response(serializer.data)
