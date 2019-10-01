from django.test import TestCase
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Movement
# Create your tests here.


class MovementTests(APITestCase):

    def setUp(self):
        self.products = [
            {'name': 'Water', 'price': "2.50", 'sku': 'WATER-500'},
            {'name': 'Soda', 'price': "4.00", 'sku': 'SODA-350'},
            {'name': 'Sugar', 'price': "3.00", 'sku': 'SUGAR-1000'}
        ]
        for values, klass in [(self.products, Product)]:
            for props in values:
                klass.objects.create(**props)

    def test_create_mov(self):
        url = reverse('movement-list')
        data = {
            'product': reverse('product-detail', args=[Product.objects.get(name='Water').id]),
            'quantity': 5,
            'kind': Movement.IN
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movement.objects.count(), 1)
        self.assertEqual(Product.objects.get(name='Water').quantity, 5)

        data = {
            'product': reverse('product-detail', args=[Product.objects.get(name='Water').id]),
            'quantity': 6,
            'kind': Movement.OUT
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Movement.objects.count(), 1)
        self.assertEqual(Product.objects.get(name='Water').quantity, 5)
