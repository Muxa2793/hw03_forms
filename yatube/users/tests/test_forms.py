from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class PostFormTests(TestCase):
    def setUp(self):
        # Create authorized clients
        self.guest_client = Client()

    def test_create_new_post_through_the_form(self):
        user_count_before = User.objects.count()

        password = User.objects.make_random_password()
        form_data = {
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test',
            'email': 'test@test.ru',
            'password1': password,
            'password2': password,
        }

        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True,
        )

        user_count_after = User.objects.count()
        self.assertEqual(user_count_after, user_count_before + 1)

        self.assertTrue(User.objects.filter(username='test').exists())

        redirect_adress = reverse('posts:index')
        self.assertRedirects(response, redirect_adress)
