from django.test import Client, TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from app.settings import STATICFILES_DIRS, BASE_DIR
from app.views import home, discography, tour, members
from app.urls import urlpatterns
from bs4 import BeautifulSoup
import requests


class TestViews(TestCase):
    """
    Use the test client to get all of the views and test that the correct template was used.
    """

    def setUp(self):
        self.factory = RequestFactory()


    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(url, '/')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_discography_url(self):
        url = reverse('discography')
        self.assertEqual(url, '/discography')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discography.html')

    def test_discography_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/discography')
        response = discography(request)
        self.assertEqual(response.status_code, 200)

    def test_members_url(self):
        url = reverse('members')
        self.assertEqual(url, '/members')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members.html')

    def test_members_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/members')
        response = members(request)
        self.assertEqual(response.status_code, 200)

    def test_tour_url(self):
        url = reverse('tour')
        self.assertEqual(url, '/tour')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tour.html')

    def test_tour_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/tour')
        response = tour(request)
        self.assertEqual(response.status_code, 200)

    def test_static_config(self):
        """
        Tests the static file configuration to make sure
        that the app looks in the static folder paths.
        """
        result = finders.find('dummy_filename')
        searched_locations = finders.searched_locations
        for d in STATICFILES_DIRS:
            self.assertIn(d, searched_locations)

    def test_base_navbar_urls(self):
        response = self.client.get('/')
        self.assertContains(response, reverse('members'))
        self.assertContains(response, reverse('discography'))
        self.assertContains(response, reverse('home'))
        self.assertContains(response, reverse('tour'))

    def test_broken_links(self):
        def check_link(href):
            if "//" in href:
                self.assertEqual(requests.get(href).status_code, 200)
            elif '/static/' in href:
                # remove static for django
                static = href.replace('/static/', '')
                self.assertIsNotNone(finders.find(static))
            else:
                self.assertEqual(self.client.get(href).status_code, 200)

        for pattern in urlpatterns:
            url = reverse(pattern.name)
            response = self.client.get(url)
            soup = BeautifulSoup(str(response))
            a = soup.find_all('a')
            for link in a:
                # get link address
                href = link.get('href')

                if href is None or len(href) == 0 or href[0] == '#':
                    continue

                check_link(href)

            img = soup.find_all('img')
            for link in img:
                href = link.get('src')
                if href is None or len(href) == 0 or href[0] == '#':
                    continue

                check_link(href)



