from urllib.parse import urlencode

from django.urls import reverse
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Movie, Comment


class TestMovies(APITestCase):

    def setUp(self):
        self.url = reverse('Movie-list')

    def test_add_movie(self):
        response = self.client.post(self.url, {"title": "batman"})
        eq_(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("title" in response.json())

        response = self.client.post(self.url, {"title": "spiderman"})
        eq_(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("title" in response.json())

        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

        response = self.client.get(reverse('Movie-list', args=(1,)))
        self.assertEqual(len(response.json()), 1)


class TestComment(APITestCase):
    def setUp(self):
        self.url = reverse('Comment-list')

        movie_url = reverse('Movie-list')

        response = self.client.post(movie_url, {"title": "batman"})
        eq_(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("title" in response.json())

        response = self.client.post(movie_url, {"title": "spiderman"})
        eq_(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("title" in response.json())

    def test_add_comment(self):
        movie_id = 1
        response = self.client.post(self.url, {"movie": movie_id,
                                               "body": "foobar"})
        eq_(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("body" in response.json())

        response = self.client.post(self.url, {"movie": movie_id,
                                               "body": "foobar2"})
        eq_(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("body" in response.json())

        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

        response = self.client.get(self.url + "?" + urlencode({'movie': movie_id}))
        eq_(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

        response = self.client.get(self.url + "?" + urlencode({'movie': 2}))
        eq_(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

        response = self.client.get(reverse('Comment-list', args=(1,)))
        self.assertEqual(len(response.json()), 1)