from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import ProductMaster, StockMain, StockDetail
from .forms import ProductForm, StockMainForm, CustomStockDetailFormSet

@login_required
def dashboard(request):
    """Main dashboard showing inventory overview"""
    products = ProductMaster.objects.all()
    recent_transactions = StockMain.objects.all()[:10]
    
    # Calculate inventory summary
    total_products = products.count()
    total_transactions = StockMain.objects.count()
    low_stock_products = [p for p in products if p.get_current_stock() <= 5]
    
    context = {
        'products': products,
        'recent_transactions': recent_transactions,
        'total_products': total_products,
        'total_transactions': total_transactions,
        'low_stock_count': len(low_stock_products),
        'low_stock_products': low_stock_products,
    }
    return render(request, 'home/dashboard.html', context)

@login_required
def product_list(request):
    """Display all products with current stock levels"""
    products = ProductMaster.objects.all()
    products_with_stock = []
    
    for product in products:
        products_with_stock.append({
            'product': product,
            'current_stock': product.get_current_stock()
        })
    
    context = {
        'products_with_stock': products_with_stock,
    }
    return render(request, 'home/product_list.html', context)

@login_required
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'home/add_product.html', {'form': form})

@login_required
def transaction_list(request):
    """Display all stock transactions"""
    transactions = StockMain.objects.all()
    return render(request, 'home/transaction_list.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    """Add new stock transaction"""
    if request.method == 'POST':
        main_form = StockMainForm(request.POST)
        if main_form.is_valid():
            try:
                with transaction.atomic():
                    stock_main = main_form.save()
                    formset = CustomStockDetailFormSet(
                        request.POST, 
                        instance=stock_main,
                        transaction_type=stock_main.type
                    )
                    
                    if formset.is_valid():
                        formset.save()
                        messages.success(request, 'Transaction added successfully!')
                        return redirect('transaction_list')
                    else:
                        # If formset is invalid, delete the main transaction
                        stock_main.delete()
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        main_form = StockMainForm()
        formset = CustomStockDetailFormSet()
    
    context = {
        'main_form': main_form,
        'formset': formset,
    }
    return render(request, 'home/add_transaction.html', context)

@login_required
def transaction_detail(request, pk):
    """View details of a specific transaction"""
    stock_transaction = get_object_or_404(StockMain, pk=pk)
    details = stock_transaction.details.all()
    
    context = {
        'transaction': stock_transaction,
        'details': details,
    }
    return render(request, 'home/transaction_detail.html', context)

@login_required
def inventory_report(request):
    """Generate inventory report"""
    products = ProductMaster.objects.all()
    inventory_data = []
    
    total_value = 0
    for product in products:
        current_stock = product.get_current_stock()
        inventory_data.append({
            'product': product,
            'current_stock': current_stock,
            'status': 'Low Stock' if current_stock <= 5 else 'In Stock' if current_stock > 0 else 'Out of Stock'
        })
    
    context = {
        'inventory_data': inventory_data,
    }
    return render(request, 'home/inventory_report.html', context)

@login_required
def get_product_stock(request, product_id):
    """AJAX endpoint to get current stock of a product"""
    try:
        product = ProductMaster.objects.get(id=product_id)
        current_stock = product.get_current_stock()
        return JsonResponse({
            'success': True,
            'current_stock': current_stock,
            'product_name': product.name
        })
    except ProductMaster.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Product not found'
        })

def home(request):
    return redirect('dashboard')
