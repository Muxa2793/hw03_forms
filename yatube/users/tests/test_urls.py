from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersURLTest(TestCase):
    '''Test Users url for exisitng.'''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Сreating test users for testing
        cls.user = User.objects.create_user(username='user',
                                            email='test@test.ru')

    def setUp(self):
        # Create unauthorized client
        self.guest_client = Client()
        # Create authorized clients
        self.authorized_client = Client()
        self.authorized_client.force_login(UsersURLTest.user)
        self.url_data = {'uidb64': 'uidb64', 'token': 'token'}

    def test_logout_existing(self):
        adress = reverse('users:logout')
        response = self.authorized_client.get(adress)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_and_singup_existing(self):
        adresses = [
            reverse('users:signup'),
            reverse('users:login'),
        ]

        for adress in adresses:
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_forms_existing(self):
        adresses = [
            reverse('users:password_reset_form'),
            reverse('users:password_reset_done'),
            reverse('users:password_change_form'),
            reverse('users:password_change_done'),
            reverse('users:password_reset_confirm', kwargs=self.url_data),
            reverse('users:password_reset_complete'),
        ]

        for adress in adresses:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_auth_users_templates(self):
        '''Testing correct templates for auth users.'''
        templates_url_names = {
            reverse('users:logout'): 'users/logged_out.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_not_auth_users_templates(self):
        '''Testing correct templates for not auth users.'''
        templates_url_names = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_password_forms_templates(self):
        '''Testing correct templates for password forms.'''
        templates_url_names = {
            reverse('users:password_reset_form'):
                'users/password_reset_form.html',
            reverse('users:password_reset_done'):
                'users/password_reset_done.html',
            reverse('users:password_change_form'):
                'users/password_change_form.html',
            reverse('users:password_change_done'):
                'users/password_change_done.html',
            reverse('users:password_reset_confirm', kwargs=self.url_data):
                'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'):
                'users/password_reset_complete.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
