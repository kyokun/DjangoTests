# -*- coding: utf-8 -*-
"""Static tests."""

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Category


class TestCategory(APITestCase):
    """Category tests."""
    fixtures = ['category']

    def test_get_categories(self):
        """Return all the categories created."""
        response = self.client.get(reverse('api:category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 5)

    def test_create_category(self):
        """Ensure we can create a new category object."""
        url = reverse('api:category-list')
        data = {'name': 'Tech'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 6)
        self.assertEqual(Category.objects.get(pk=6).name, 'Tech')

    def test_create_wrong_category(self):
        """
        Ensure we can not create a new category object with wrong data,
        should return 400 bad request.
        """
        url = reverse('api:category-list')
        data = {'name': 'Tech', 'status': 'Waiting'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(), 5)

    def test_get_specific_category(self):
        """Ensure we can retrieve category object."""
        url = reverse('api:category-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': '1',
                                         'status': False})

    def test_get_unexisting_category(self):
        """
        Ensure we can not retrieve an unexisting category,
        should return 404 not found.
        """
        url = reverse('api:category-detail', kwargs={'pk': 10})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category(self):
        """Ensure we can update a category object."""
        url = reverse('api:category-detail', kwargs={'pk': 2})
        data = {'name': 'New category', 'status': True}
        response = self.client.put(url, data)
        category = Category.objects.get(pk=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(category.name, 'New category')
        self.assertIs(category.status, True)

    def test_partial_update_category(self):
        """Ensure we can update partially a category object."""
        url = reverse('api:category-detail', kwargs={'pk': 3})
        data = {'status': True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIs(Category.objects.get(pk=3).status, True)

    def test_partial_update_wrong_category(self):
        """
        Ensure we can not update partially a category object with wrong data,
        should return 400 bad request.
        """
        url = reverse('api:category-detail', kwargs={'pk': 3})
        data = {'status': 'Active'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIs(Category.objects.get(pk=3).status, False)

    def test_delete_specific_category(self):
        """Ensure we can delete a category object."""
        url = reverse('api:category-detail', kwargs={'pk': 5})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 4)

    def test_delete_unexisting_category(self):
        """
        Ensure we can not delete an unexisting category object,
        should return 404 not found.
        """
        url = reverse('api:category-detail', kwargs={'pk': 10})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Category.objects.count(), 5)
