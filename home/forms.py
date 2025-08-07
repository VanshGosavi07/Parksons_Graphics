from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.core.exceptions import ValidationError
from .models import ProductMaster, StockMain, StockDetail

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductMaster
        fields = ['name', 'description', 'sku']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter product description (optional)'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unique SKU', 'required': True}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) < 2:
            raise ValidationError("Product name must be at least 2 characters long.")
        return name.strip()
    
    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku:
            raise ValidationError("SKU is required.")
        
        sku = sku.strip().upper()
        
        # Check if SKU already exists (excluding current instance if editing)
        existing_product = ProductMaster.objects.filter(sku=sku)
        if self.instance and self.instance.pk:
            existing_product = existing_product.exclude(pk=self.instance.pk)
        
        if existing_product.exists():
            raise ValidationError("A product with this SKU already exists.")
        
        # Validate SKU format (alphanumeric with hyphens allowed)
        import re
        if not re.match(r'^[A-Z0-9\-]+$', sku):
            raise ValidationError("SKU can only contain uppercase letters, numbers, and hyphens.")
        
        if len(sku) < 3:
            raise ValidationError("SKU must be at least 3 characters long.")
        
        return sku

class StockMainForm(forms.ModelForm):
    class Meta:
        model = StockMain
        fields = ['type', 'remarks']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter remarks (optional)'}),
        }
    
    def clean_type(self):
        transaction_type = self.cleaned_data.get('type')
        if transaction_type not in ['IN', 'OUT']:
            raise ValidationError("Invalid transaction type. Must be 'IN' or 'OUT'.")
        return transaction_type

class StockDetailForm(forms.ModelForm):
    class Meta:
        model = StockDetail
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Enter quantity', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)
        
        # Ensure we have products to choose from
        if not ProductMaster.objects.exists():
            self.fields['product'].widget.attrs['disabled'] = True
            self.fields['product'].help_text = "No products available. Please add products first."
        
        # Add validation for stock out
        if transaction_type == 'OUT':
            self.fields['quantity'].help_text = "Make sure quantity doesn't exceed available stock"

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise ValidationError("Please select a product.")
        return product

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if not quantity or quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        if quantity > 10000:  # Reasonable upper limit
            raise ValidationError("Quantity cannot exceed 10,000 units.")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        # Get transaction type from the form's parent if available
        if hasattr(self, 'transaction_type'):
            transaction_type = self.transaction_type
        else:
            # Try to get from the main form in the context
            transaction_type = getattr(self, '_transaction_type', None)
        
        if product and quantity and transaction_type == 'OUT':
            current_stock = product.get_current_stock()
            if quantity > current_stock:
                raise ValidationError(
                    f"Cannot remove {quantity} units of {product.name}. "
                    f"Only {current_stock} units available in stock."
                )
        
        return cleaned_data

# Enhanced formset with custom validation
StockDetailFormSet = inlineformset_factory(
    StockMain, 
    StockDetail, 
    form=StockDetailForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)

class CustomStockDetailFormSet(StockDetailFormSet):
    def __init__(self, *args, **kwargs):
        self.transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)
        
        # Pass transaction type to all forms
        for form in self.forms:
            form._transaction_type = self.transaction_type
    
    def clean(self):
        """Validate the entire formset"""
        if any(self.errors):
            return
        
        products = []
        total_quantity = 0
        
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                product = form.cleaned_data.get('product')
                quantity = form.cleaned_data.get('quantity', 0)
                
                if product:
                    # Check for duplicate products
                    if product in products:
                        raise ValidationError("Each product can only appear once per transaction.")
                    products.append(product)
                    total_quantity += quantity
        
        if not products:
            raise ValidationError("At least one product must be included in the transaction.")
        
        if total_quantity <= 0:
            raise ValidationError("Total quantity must be greater than 0.")
