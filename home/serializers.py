from rest_framework import serializers
from .models import ProductMaster, StockMain, StockDetail

class ProductMasterSerializer(serializers.ModelSerializer):
    current_stock = serializers.ReadOnlyField(source='get_current_stock')
    
    class Meta:
        model = ProductMaster
        fields = ['id', 'name', 'description', 'sku', 'current_stock', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'current_stock']
    
    def validate_sku(self, value):
        """Ensure SKU is unique"""
        # Convert to uppercase for consistency
        value = value.upper().strip()
        
        # Check for existing SKU, excluding current instance if updating
        queryset = ProductMaster.objects.filter(sku=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A product with this SKU already exists.")
        
        # Validate SKU format
        import re
        if not re.match(r'^[A-Z0-9\-]+$', value):
            raise serializers.ValidationError("SKU can only contain uppercase letters, numbers, and hyphens.")
        
        if len(value) < 3:
            raise serializers.ValidationError("SKU must be at least 3 characters long.")
        
        return value

    def validate_name(self, value):
        """Validate product name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Product name must be at least 2 characters long.")
        return value.strip()

class StockDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_sku = serializers.ReadOnlyField(source='product.sku')
    
    class Meta:
        model = StockDetail
        fields = ['id', 'product', 'product_name', 'product_sku', 'quantity']
    
    def validate_quantity(self, value):
        """Ensure quantity is positive and within reasonable limits"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if value > 10000:
            raise serializers.ValidationError("Quantity cannot exceed 10,000 units.")
        return value
    
    def validate(self, data):
        """Validate stock out doesn't exceed available stock"""
        if hasattr(self, 'instance') and self.instance:
            # This is an update - get transaction from instance
            transaction = self.instance.transaction
        else:
            # This is creation - transaction should be provided in context
            transaction = self.context.get('transaction')
        
        if transaction and transaction.type == 'OUT':
            product = data.get('product')
            quantity = data.get('quantity')
            
            if product and quantity:
                current_stock = product.get_current_stock()
                if quantity > current_stock:
                    raise serializers.ValidationError(
                        f"Cannot remove {quantity} {product.name}. Only {current_stock} available in stock."
                    )
        
        return data

class StockMainSerializer(serializers.ModelSerializer):
    details = StockDetailSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField(source='get_total_items')
    
    class Meta:
        model = StockMain
        fields = ['id', 'date', 'type', 'remarks', 'total_items', 'details', 'created_at']
        read_only_fields = ['created_at', 'total_items', 'details']

class StockTransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating transactions with details"""
    details = StockDetailSerializer(many=True)
    
    class Meta:
        model = StockMain
        fields = ['type', 'remarks', 'details']
    
    def validate_details(self, value):
        """Ensure at least one product detail is provided and no duplicates"""
        if not value:
            raise serializers.ValidationError("At least one product must be included in the transaction.")
        
        # Check for duplicate products in the same transaction
        product_ids = [detail.get('product').id if detail.get('product') else None for detail in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Each product can only appear once per transaction.")
        
        return value

    def validate_type(self, value):
        """Validate transaction type"""
        if value not in ['IN', 'OUT']:
            raise serializers.ValidationError("Transaction type must be either 'IN' or 'OUT'.")
        return value
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        stock_main = StockMain.objects.create(**validated_data)
        
        for detail_data in details_data:
            # Add transaction context for validation
            detail_serializer = StockDetailSerializer(data=detail_data, context={'transaction': stock_main})
            if detail_serializer.is_valid(raise_exception=True):
                detail_serializer.save(transaction=stock_main)
        
        return stock_main

class InventoryReportSerializer(serializers.Serializer):
    """Serializer for inventory report data"""
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_sku = serializers.CharField()
    product_description = serializers.CharField(allow_blank=True)
    current_stock = serializers.IntegerField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
