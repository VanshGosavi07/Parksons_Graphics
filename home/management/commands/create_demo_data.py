from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import ProductMaster, StockMain, StockDetail
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create demo data for the warehouse inventory system'
    
    def handle(self, *args, **options):
        # Create demo user
        if not User.objects.filter(username='demo').exists():
            user = User.objects.create_user(
                username='demo',
                email='demo@warehouse.com',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'Created demo user: demo/demo123'))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists'))
        
        # Create demo admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@warehouse.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin/admin123'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        # Create demo products
        products_data = [
            {'name': 'Laptop Computer', 'sku': 'LAPTOP-001', 'description': 'Dell Inspiron 15 3000 Series'},
            {'name': 'Wireless Mouse', 'sku': 'MOUSE-001', 'description': 'Logitech M170 Wireless Mouse'},
            {'name': 'USB Cable', 'sku': 'CABLE-001', 'description': 'USB Type-C to USB-A Cable'},
            {'name': 'Monitor Stand', 'sku': 'STAND-001', 'description': 'Adjustable Monitor Stand'},
            {'name': 'Keyboard', 'sku': 'KEYB-001', 'description': 'Mechanical Gaming Keyboard'},
        ]
        
        created_products = []
        for product_data in products_data:
            product, created = ProductMaster.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description']
                }
            )
            if created:
                created_products.append(product)
                self.stdout.write(f'Created product: {product.name}')
        
        if created_products:
            # Create initial stock transactions
            stock_in = StockMain.objects.create(
                type='IN',
                remarks='Initial stock inventory'
            )
            
            for product in created_products:
                StockDetail.objects.create(
                    transaction=stock_in,
                    product=product,
                    quantity=50
                )
            
            self.stdout.write(self.style.SUCCESS('Created demo products and initial stock'))
        else:
            self.stdout.write(self.style.WARNING('Demo products already exist'))
        
        self.stdout.write(self.style.SUCCESS('Demo data setup completed!'))
        self.stdout.write('Access the application at: http://127.0.0.1:8000')
        self.stdout.write('Login credentials:')
        self.stdout.write('  - Demo user: demo/demo123')
        self.stdout.write('  - Admin user: admin/admin123')
