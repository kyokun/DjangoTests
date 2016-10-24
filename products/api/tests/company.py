# -*- coding: utf-8 -*-
"""Company tests."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models.company import Company

website = 'https://github.com/lnphi'
state = 1
country = 1
industry = 1
categories = [1, 2, 4]


class TestCompany(APITestCase):
    """Company tests."""
    fixtures = ['category', 'country', 'industry', 'state',
                'api/tests/fixtures/company']

    def test_get_companies(self):
        """Ensure we can retrieve all company objects."""
        response = self.client.get(reverse('api:company-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 3)

    def test_create_company(self):
        """Ensure we can create a new company object."""
        url = reverse('api:company-list')
        data = {'business_name': 'Ln(phi)', 'website': website, 'address': {
            'street': 'Chihuahua',
            'num_ext': '1',
            'zip_code': '1',
            'state': state,
            'country': country
        }, 'main_phone': {
            'number': '55010203',
            'name': 'Main',
            'extension': '01',
            'country': country
        }, 'industry': industry, 'product_categories': categories}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 4)

    def test_create_company_with_the_same_business_name(self):
        """
        Ensure we can not create a new company object if the business_name
        already exists.
        """
        url = reverse('api:company-list')
        data = {'business_name': 'dw', 'website': website, 'address': {
            'street': 'Chihuahua',
            'num_ext': '1',
            'zip_code': '1',
            'state': state,
            'country': country
        }, 'main_phone': {
            'number': '55010203',
            'name': 'Main',
            'extension': '01',
            'country': country
        }, 'industry': industry, 'product_categories': categories}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 3)

    def test_create_company_with_invalid_website_url(self):
        """
        Ensure we can not create a new company object with wrong data,
        should return 400 bad request.
        """
        url = reverse('api:company-list')
        website = 'lnphi123'
        data = {'business_name': 'Ln(phi)', 'website': website, 'address': {
            'street': 'Chihuahua',
            'num_ext': '1',
            'zip_code': '1',
            'state': state,
            'country': country
        }, 'main_phone': {
            'number': '55010203',
            'name': 'Main',
            'extension': '01',
            'country': country
        }, 'industry': industry, 'product_categories': categories}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 3)

    def test_create_company_with_unexisting_country(self):
        """
        Ensure we can not create a new company object with wrong data,
        should return 400 bad request.
        """
        url = reverse('api:company-list')
        country = 2
        data = {
            'business_name': 'Ln(phi)', 'website': website,
            'address': {
                'street': 'Chihuahua',
                'num_ext': '1',
                'zip_code': '1',
                'state': state,
                'country': country
            }, 'main_phone': {
                'number': '55010203',
                'name': 'Main',
                'extension': '01',
                'country': country
            }, 'industry': industry, 'product_categories': categories
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 3)

    def test_create_company_with_unexisting_categories(self):
        """
        Ensure we can not create a new company object with wrong data,
        should return 400 bad request.
        """
        url = reverse('api:company-list')
        categories = ['a', 'b']
        data = {
            'business_name': 'Ln(phi)', 'website': 'https://github.com/lnphi',
            'address': {
                'street': 'Chihuahua',
                'num_ext': '1',
                'zip_code': '1',
                'state': state,
                'country': country
            }, 'main_phone': {
                'number': '55010203',
                'name': 'Main',
                'extension': '01',
                'country': country
            }, 'industry': industry, 'product_categories': categories
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 3)

    def test_create_company_with_malformed_json(self):
        """
        Ensure we can not create a new company object with wrong data,
        should return 400 bad request.
        """
        url = reverse('api:company-list')
        data = {
            'business_name': 'Ln(phi)', 'website': 'https://github.com/lnphi',
            'street': 'Chihuahua', 'num_ext': '1', 'zip_code': '1',
            'state': state, 'country': country, 'number': '55010203',
            'name': 'Main', 'extension': '01', 'country': country,
            'industry': industry, 'product_categories': categories
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.count(), 3)

    def test_get_detail_company(self):
        """Ensure we can retrieve a company object."""
        url = reverse('api:company-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['business_name'], 'dw')
        self.assertEqual(response.data['address']['zip_code'], '123')
        self.assertEqual(response.data['main_phone']['name'], '132')

    def test_get_unexisting_company(self):
        """
        Ensure we can not retrieve an unexisting company,
        should return 404 not found.
        """
        url = reverse('api:company-detail', kwargs={'pk': 10})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_company(self):
        """Ensure we can update a company object."""
        business_name = 'Ln(phi)'
        state = 2
        url = reverse('api:company-detail', kwargs={'pk': 2})
        data = {
            'business_name': business_name,
            'address': {
                'state': state
            }
        }
        response = self.client.patch(url, data, format='json')
        company = Company.objects.get(pk=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(company.business_name, business_name)
        self.assertEqual(company.state_id, state)

    def test_update_wrong_company(self):
        """
        Ensure we can not update a company object with wrong data,
        should return 400 bad request.
        """
        url = reverse('api:company-detail', kwargs={'pk': 3})
        data = {
            'website': 'I am wrong'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Company.objects.get(pk=3).phone_country_id, 1)

    def test_delete_specific_company(self):
        """Ensure we can delete a company object."""
        url = reverse('api:company-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 2)

    def test_delete_unexisting_company(self):
        """
        Ensure we can not delete an unexisting company object,
        should return 404 not found.
        """
        url = reverse('api:company-detail', kwargs={'pk': 10})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Company.objects.count(), 3)
