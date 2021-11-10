from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class ViewTests(TestCase):
    '''Testing templates and context for view func in post app.'''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Сreating test users for testing
        cls.user = User.objects.create_user(username='user')
        cls.user_author = User.objects.create_user(username='user_author')
        cls.user_author_2 = User.objects.create_user(username='user_author_2')

        # Сreating test group for testing group templates
        cls.group = Group.objects.bulk_create(
            [
                Group(
                    id=3,
                    title='Тестовая группа id = 3',
                    slug='test-slug-one',
                    description='Тестовое описание',
                ),
                Group(
                    id=2,
                    title='Тестовая группа id = 2',
                    slug='test-slug-second',
                    description='Тестовое описание',
                ),
            ]
        )

        # Сreating test post for testing post templates
        cls.post = Post.objects.bulk_create(
            [
                Post(
                    id=3,
                    text='тестовый текст id = 3',
                    author=cls.user_author,
                    group=cls.group[0],
                ),
                Post(
                    id=2,
                    text='тестовый текст id = 2',
                    author=cls.user_author,
                    group=cls.group[1],
                ),
                Post(
                    id=1,
                    text='тестовый текст id = 1',
                    author=cls.user_author_2,
                ),
            ]
        )

    def setUp(self):
        # Create authorized clients
        self.authorized_client = Client()
        self.authorized_client_author = Client()
        self.authorized_client.force_login(ViewTests.user)
        self.authorized_client_author.force_login(ViewTests.user_author)

        # Get slug for group urls
        self.slug = {'slug': ViewTests.group[0].slug}
        # Get username for profile url
        self.user = {'username': ViewTests.user.username}
        self.user_author = {'username': ViewTests.user_author.username}
        # Get post_id gor post detail url
        self.post_id = {'post_id': ViewTests.post[0].id}

    def test_pages_uses_correct_template(self):
        '''Testing templates'''
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts', kwargs=self.slug): (
                'posts/group_list.html'
            ),
            reverse('posts:profile', kwargs=self.user): (
                'posts/profile.html'
            ),
            reverse('posts:post_detail', kwargs=self.post_id): (
                'posts/post_detail.html'
            ),
            reverse('posts:post_edit', kwargs=self.post_id): (
                'posts/create_post.html'
            ),
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

    def test_index_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))

        first_object = response.context['page_obj'][2]

        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group

        # check first object
        self.assertEqual(post_text_0, 'тестовый текст id = 3')
        self.assertEqual(post_author_0, ViewTests.user_author)
        self.assertEqual(post_group_0, ViewTests.group[0])

        second_object = response.context['page_obj'][1]

        post_text_1 = second_object.text
        post_author_1 = second_object.author
        post_group_1 = second_object.group

        # check second object
        self.assertEqual(post_text_1, 'тестовый текст id = 2')
        self.assertEqual(
            post_author_1,
            ViewTests.post[0].author
        )
        self.assertEqual(post_group_1, ViewTests.group[1])

        # check ordering by pub_date
        self.assertTrue(second_object.pub_date > first_object.pub_date)

    def test_group_posts_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:group_posts', kwargs=self.slug)
        )

        first_object = response.context['page_obj'][0]

        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group

        self.assertEqual(post_text_0, 'тестовый текст id = 3')
        self.assertEqual(post_author_0, ViewTests.user_author)
        self.assertEqual(post_group_0, ViewTests.group[0])

        # check that group names in two objects are different
        self.assertTrue(post_group_0 != ViewTests.group[1])

        # check that only one object in the page
        self.assertTrue(len(response.context['page_obj']) == 1)

    def test_profile_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs=self.user_author)
        )

        first_object = response.context['page_obj'][1]

        post_text_0 = first_object.text
        post_author_0 = first_object.author
        post_group_0 = first_object.group

        self.assertEqual(post_text_0, 'тестовый текст id = 3')
        self.assertEqual(post_author_0, ViewTests.user_author)
        self.assertEqual(post_group_0, ViewTests.group[0])

        second_object = response.context['page_obj'][0]
        post_author_0 = first_object.author

        # check that only two objects in the page
        self.assertTrue(len(response.context['page_obj']) == 2)

        # check that author on all posts in page is the same
        self.assertTrue(first_object.author == second_object.author)

        # check that author in the first object
        # and object with id == 1 not the same
        self.assertTrue(first_object.author != ViewTests.post[2].author)

    def test_post_detail_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs=self.post_id)
        )

        post = response.context['post']

        post_text = post.text
        post_author = post.author
        post_group = post.group
        post_id = post.id

        self.assertEqual(post_text, 'тестовый текст id = 3')
        self.assertEqual(post_author, ViewTests.user_author)
        self.assertEqual(post_group, ViewTests.group[0])
        self.assertEqual(post_id, ViewTests.post[0].id)

        # check that variable post match with object with id == 3
        self.assertEqual(post, ViewTests.post[0])

    def test_post_create_show_correct_form(self):
        response = self.authorized_client_author.get(
            reverse('posts:post_create')
        )

        form = response.context['form']

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_form(self):
        response = self.authorized_client_author.get(
            reverse('posts:post_edit', kwargs=self.post_id)
        )

        form = response.context['form']

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    '''Testing paginator view func in post app.'''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Сreating test users for testing
        cls.user = User.objects.create_user(username='user')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        # Сreating test post for testing post templates
        cls.post = Post.objects.bulk_create(
            [
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
                Post(text='тест', author=cls.user, group=cls.group),
            ]
        )

    def setUp(self):
        # Create authorized clients
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)
        # Get slug for group urls
        self.slug = {'slug': PaginatorViewsTest.group.slug}
        # Get username for profile url
        self.user = {'username': PaginatorViewsTest.user.username}

    def test_first_page_contains_ten_records(self):
        adresses = (
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs=self.slug),
            reverse('posts:profile', kwargs=self.user),
        )

        for adress in adresses:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                len_page_obj = len(response.context['page_obj'])
                self.assertEqual(len_page_obj, 10)

    def test_second_page_contains_three_records(self):
        adresses = (
            reverse('posts:index') + '?page=2',
            reverse('posts:group_posts', kwargs=self.slug) + '?page=2',
            reverse('posts:profile', kwargs=self.user) + '?page=2',
        )

        for adress in adresses:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                len_page_obj = len(response.context['page_obj'])
                self.assertEqual(len_page_obj, 3)
