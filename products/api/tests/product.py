# -*- encoding: utf-8 -*-
"""Product tests."""

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Product


class TestProduct(APITestCase):
    """Product tests."""
    fixtures = ['category', 'country', 'api/tests/fixtures/product',
                'api/tests/fixtures/attribute', 'api/tests/fixtures/keyword',
                'api/tests/fixtures/productattribute',
                'api/tests/fixtures/productextrainfo']

    def test_retrieve_all_products(self):
        """Return all the products created."""
        response = self.client.get(reverse('api:product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 3)

    def test_retrieve_one_product(self):
        """Return a specific product."""
        url = reverse('api:product-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sportflix')
        self.assertEqual(response.data['brand'], 'Ln(Phi)')
        self.assertEqual(response.data['price'], 200)

    def test_retrieve_one_product_with_invalid_data(self):
        """
        Ensure we can not retrieve a product providing invalid data,
        :return: 404 not found.
        """
        url = reverse('api:product-detail', kwargs={'pk': 4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        """
        Ensure we can create new products providing valid data,
        :return: 201 created.
        """
        data = {
            "name": "PaySensei",
            "model": "Primero",
            "brand": "Ln(Phi)",
            "price": 200,
            "category": 1,
            "made_in": 1,
            "keywords": [
                {
                    "name": "aventura"
                },
                {
                    "name": "deporte"
                }
            ],
            "attributes": [
                {
                    "name": "color",
                    "value": "rojo"
                },
                {
                    "name": "material",
                    "value": "acero"
                }
            ]
        }
        response = self.client.post(reverse('api:product-list'), data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_with_invalid_data(self):
        """
        Ensure we can not create new products providing invalid data
        :return: 400 bad request.
        """
        data = {
            "name": "PaySensei",
            "brand": "Ln(Phi)",
            "price": 200,
            "category": 0,
            "keywords": [
                {
                    "name": "aventura"
                },
                {
                    "name": "deporte"
                }
            ],
            "attributes": [
                {
                    "name": "color",
                    "value": "rojo"
                },
                {
                    "name": "material",
                    "value": "acero"
                }
            ]
        }
        response = self.client.post(reverse('api:product-list'), data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_with_extras(self):
        """
        Ensure we can update products providing extras field
        :return: 200 ok.
        """
        data = {
            "extras": [
                {
                    "title": "Titulo",
                    "description": "descripion"
                },
                {
                    "title": "otro titulo",
                    "description": "otra descripcion"
                }
            ]
        }
        response = self.client.patch(reverse('api:product-detail',
                                             kwargs={'pk': 1}),
                                     data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(data, response.data)
        self.assertTrue(response.data.get('flags').get('extras'))

    def test_update_product_with_logistics(self):
        """
        Ensure we can update products providing logistics field
        :return: 200 ok.
        """
        data = {
            "logistics": [
                {
                    "origin": 1,
                    "quantity": 20,
                    "period": "D"
                },
                {
                    "origin": 1,
                    "quantity": 100,
                    "period": "M"
                }
            ]
        }
        response = self.client.patch(reverse('api:product-detail',
                                             kwargs={'pk': 2}),
                                     data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('flags').get('logistics'))

    def test_update_product_and_complete(self):
        """
        Ensure we can update products providing logistics field
        :return: 200 ok.
        """
        data = {
            "logistics": [
                {
                    "origin": 1,
                    "quantity": 20,
                    "period": "D"
                },
                {
                    "origin": 1,
                    "quantity": 100,
                    "period": "M"
                }
            ]
        }
        response = self.client.patch(reverse('api:product-detail',
                                             kwargs={'pk': 3}),
                                     data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('flags').get('complete'))
        self.assertTrue(response.data.get('flags').get('extras'))
        self.assertTrue(response.data.get('flags').get('logistics'))

    def test_delete_one_product(self):
        """
        Ensure we can delete a product.
        :return: 204 no content.
        """
        response = self.client.delete(reverse('api:product-detail',
                                              kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 2)

    def test_delete_unexisting_product(self):
        """
        Ensure we can not delete a product if it does not exist
        :return: 404 not found.
        """
        response = self.client.delete(reverse('api:product-detail',
                                              kwargs={'pk': 5}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.count(), 3)
