from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostsURLTest(TestCase):
    '''Test Posts url for exisitng and availability and redirecting
    for any types of users.
    '''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Сreating test users for testing
        cls.user = User.objects.create_user(username='user')
        cls.user_author = User.objects.create_user(username='user_author')

        # Сreating test group for testing availability some urls
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        # Сreating test post for testing availability some urls
        cls.post = Post.objects.create(
            text='тестовыйтекст' * 50,
            author=cls.user_author,
            group=cls.group,
        )

    def setUp(self):
        # Create unauthorized client
        self.guest_client = Client()
        # Create authorized clients
        self.authorized_client = Client()
        self.authorized_client_author = Client()
        self.authorized_client.force_login(PostsURLTest.user)
        self.authorized_client_author.force_login(PostsURLTest.user_author)

        # Get slug for group urls
        self.slug = {'slug': PostsURLTest.group.slug}
        # Get username for profile url
        self.user = {'username': PostsURLTest.user.username}
        # Get post_id gor post detail url
        self.post_id = {'post_id': PostsURLTest.post.id}

    def test_url_exists_for_any_users(self):
        '''Testing url existing for any user for url_name in adresses.'''
        adresses = (
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs=self.slug),
            reverse('posts:profile', kwargs=self.user),
            reverse('posts:post_detail', kwargs=self.post_id),
            'unexisting_url/',
        )

        for adress in adresses:
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                if adress == 'unexisting_url/':
                    self.assertEqual(response.status_code,
                                     HTTPStatus.NOT_FOUND)
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_exists_for_author(self):
        '''Page "posts:post_edit" available for author of post.'''
        adress = reverse('posts:post_edit', kwargs=self.post_id)
        response = self.authorized_client_author.get(adress)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_redirecting(self):
        adress = reverse('posts:post_edit', kwargs=self.post_id)
        users_redirect = {
            self.authorized_client: reverse('posts:post_detail',
                                            kwargs=self.post_id),
            self.guest_client: (reverse('users:login') + '?next=' + adress),
        }

        for user, redirect_adress in users_redirect.items():
            with self.subTest(user=user):
                response = user.get(adress)
                self.assertRedirects(response, redirect_adress)

    def test_post_create_url_exists_for_auth_user(self):
        '''Page "posts:post_create" available for auth user.'''
        adress = reverse('posts:post_create')
        response = self.authorized_client.get(adress)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_url_redirect_guest_user_to_login_page(self):
        '''Page "posts:post_create" redirecting guest user to login page.'''
        adress = reverse('posts:post_create')
        response = self.guest_client.get(adress, follow=True)
        redirect_adress = reverse('users:login') + '?next=' + adress
        self.assertRedirects(response, redirect_adress)

    def test_urls_uses_correct_template(self):
        '''Testing correct templates'''
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts',
                    kwargs=self.slug): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs=self.user): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs=self.post_id): 'posts/post_detail.html',
            reverse('posts:post_edit',
                    kwargs=self.post_id): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                # Check for author of post
                if adress != reverse('posts:post_edit', kwargs=self.post_id):
                    response = self.authorized_client.get(adress)
                    self.assertTemplateUsed(response, template)
                else:
                    response = self.authorized_client_author.get(adress)
                    self.assertTemplateUsed(response, template)
