from django.contrib import admin
from .models import ProductMaster, StockMain, StockDetail

@admin.register(ProductMaster)
class ProductMasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'get_current_stock', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'sku', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_current_stock(self, obj):
        return obj.get_current_stock()
    get_current_stock.short_description = 'Current Stock'

class StockDetailInline(admin.TabularInline):
    model = StockDetail
    extra = 1

@admin.register(StockMain)
class StockMainAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'date', 'get_total_items', 'created_at']
    list_filter = ['type', 'date', 'created_at']
    search_fields = ['remarks']
    readonly_fields = ['created_at']
    inlines = [StockDetailInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

@admin.register(StockDetail)
class StockDetailAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'product', 'quantity']
    list_filter = ['transaction__type', 'product']
    search_fields = ['product__name', 'transaction__remarks']
