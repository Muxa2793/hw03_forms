from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        # Сreating test group for testing availability some urls
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        # Сreating test post for testing availability some urls
        cls.post = Post.objects.create(
            text='тестовыйтекст',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        # Create authorized clients
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)

        self.post_id = PostFormTests.post.id

    def test_create_new_post_through_the_form(self):
        post_count_before = Post.objects.count()

        form_data = {
            'text': 'тест',
            'group': PostFormTests.group.id,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        post_count_after = Post.objects.count()
        self.assertEqual(post_count_after, post_count_before + 1)

        self.assertTrue(
            Post.objects.filter(
                text='тест',
                group=PostFormTests.group,
            ).exists()
        )
        username = PostFormTests.user.username
        redirect_adress = reverse('posts:profile', args=(username,))
        self.assertRedirects(response, redirect_adress)

    def test_edit_post_through_the_form(self):
        adress = reverse('posts:post_edit', args=(self.post_id,))

        post_count_before = Post.objects.count()
        form_data = {
            'text': 'тест',
            'group': PostFormTests.group.id,
        }

        response = self.authorized_client.post(
            adress,
            data=form_data,
            follow=True,
        )

        post_count_after = Post.objects.count()
        self.assertEqual(post_count_after, post_count_before)

        self.assertTrue(
            Post.objects.filter(
                id=PostFormTests.post.id,
                text='тест',
                group=PostFormTests.group,
            ).exists()
        )

        redirect_adress = reverse('posts:post_detail', args=(self.post_id,))
        self.assertRedirects(response, redirect_adress)
