from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ProductMaster, StockMain, StockDetail

class BasicTestCase(TestCase):
    """Basic tests to ensure the application works"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_models_creation(self):
        """Test that models can be created"""
        product = ProductMaster.objects.create(
            name='Test Product',
            sku='TEST-001',
            description='Test Description'
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.get_current_stock(), 0)
    
    def test_login_required(self):
        """Test that dashboard requires authentication"""
        response = self.client.get('/')  # Test the root URL directly
        # Should redirect (either 301 or 302 is acceptable for redirects)
        self.assertIn(response.status_code, [301, 302])
        # The important thing is that unauthenticated users can't access protected content
        # Let's also test that we get redirected when trying to access product list
        response2 = self.client.get(reverse('product_list'))
        self.assertIn(response2.status_code, [301, 302])
    
    def test_login_works(self):
        """Test that login functionality works"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Should redirect after successful login (either 301 or 302 is acceptable)
        self.assertIn(response.status_code, [301, 302])
