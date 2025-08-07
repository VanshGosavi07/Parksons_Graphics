from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class ProductMaster(models.Model):
    """Product Master Table - stores the details of the products"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prodmast'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_current_stock(self):
        """Calculate current stock level for this product"""
        stock_in = StockDetail.objects.filter(
            product=self,
            transaction__type='IN'
        ).aggregate(total=models.Sum('quantity'))['total'] or 0
        
        stock_out = StockDetail.objects.filter(
            product=self,
            transaction__type='OUT'
        ).aggregate(total=models.Sum('quantity'))['total'] or 0
        
        return stock_in - stock_out

class StockMain(models.Model):
    """Stock Transaction Header Table - stores the transaction details"""
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]
    
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stckmain'
        verbose_name = 'Stock Transaction'
        verbose_name_plural = 'Stock Transactions'
        ordering = ['-date']

    def __str__(self):
        return f"{self.type} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    def get_total_items(self):
        """Get total number of items in this transaction"""
        return self.details.aggregate(total=models.Sum('quantity'))['total'] or 0

class StockDetail(models.Model):
    """Stock Transaction Detail Table - stores the details of products within each transaction"""
    transaction = models.ForeignKey(StockMain, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(ProductMaster, on_delete=models.CASCADE, related_name='stock_details')
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'stckdetail'
        verbose_name = 'Stock Detail'
        verbose_name_plural = 'Stock Details'
        unique_together = ['transaction', 'product']  # Prevent duplicate products in same transaction

    def __str__(self):
        return f"{self.product.name} - {self.quantity} ({self.transaction.type})"

    def clean(self):
        """Validate stock out doesn't exceed available stock"""
        if self.transaction.type == 'OUT':
            current_stock = self.product.get_current_stock()
            if self.quantity > current_stock:
                raise ValidationError(
                    f"Cannot remove {self.quantity} items. Only {current_stock} available in stock."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
