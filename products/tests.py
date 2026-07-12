from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Customer, Address, Order, OrderItem


class PageSmokeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_frontend_stranka(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_api_produkty(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)

    def test_admin_stranka(self):
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [200, 302])


class ProductModelTest(TestCase):
    def test_vytvoreni_produktu(self):
        p = Product.objects.create(name='BMW X5', price=1500000, stock=3)
        self.assertEqual(str(p), 'BMW X5')
        self.assertEqual(p.stock, 3)
        self.assertEqual(float(p.price), 1500000.0)

    def test_logo_url_vychozi_prazdny(self):
        p = Product.objects.create(name='Test', price=100, stock=1)
        self.assertEqual(p.logo_url, '')

    def test_logo_url_ulozeni(self):
        p = Product.objects.create(name='Audi', price=800000, stock=2, logo_url='https://example.com/logo.png')
        self.assertEqual(p.logo_url, 'https://example.com/logo.png')


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.produkt = Product.objects.create(name='Škoda Octavia', price=500000, stock=5)

    def test_seznam_produktu(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_detail_produktu(self):
        response = self.client.get(f'/api/products/{self.produkt.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Škoda Octavia')

    def test_vytvoreni_produktu(self):
        data = {'name': 'Toyota GR86', 'price': '750000.00', 'stock': 2}
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_aktualizace_produktu(self):
        data = {'name': 'Škoda Octavia', 'price': '520000.00', 'stock': 4}
        response = self.client.put(f'/api/products/{self.produkt.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produkt.refresh_from_db()
        self.assertEqual(float(self.produkt.price), 520000.0)

    def test_castecna_aktualizace(self):
        response = self.client.patch(f'/api/products/{self.produkt.id}/', {'stock': 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produkt.refresh_from_db()
        self.assertEqual(self.produkt.stock, 10)

    def test_smazani_produktu(self):
        response = self.client.delete(f'/api/products/{self.produkt.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_neexistujici_produkt(self):
        response = self.client.get('/api/products/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vytvoreni_bez_nazvu(self):
        response = self.client.post('/api/products/', {'price': '100.00', 'stock': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StockManagementTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='BMW X5', price=1500000, stock=5)
        user = User.objects.create_user(username='testuser', password='pass')
        self.customer = Customer.objects.create(user=user)
        self.address = Address.objects.create(
            customer=self.customer, street='Main 1', city='Prague', zip_code='10000'
        )
        self.order = Order.objects.create(customer=self.customer, shipping_address=self.address)
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2, unit_price=1500000)

    def test_stock_decremented_on_confirm(self):
        self.order.status = 'confirmed'
        self.order.save()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_stock_restored_on_cancel(self):
        self.order.status = 'confirmed'
        self.order.save()
        self.order.status = 'cancelled'
        self.order.save()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

    def test_stock_validation_fails_when_insufficient(self):
        self.product.stock = 1
        self.product.save()
        self.order.status = 'confirmed'
        with self.assertRaises(ValidationError):
            self.order.save()
