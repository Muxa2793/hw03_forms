from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_and_tech_page_existing(self):
        adresses = [
            reverse('about:author'),
            reverse('about:tech'),
        ]
        for adress in adresses:
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_author_and_tech_page_templates(self):
        adresses = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for adress, template in adresses.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)
