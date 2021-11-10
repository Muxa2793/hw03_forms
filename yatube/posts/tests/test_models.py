from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Group, Post

User = get_user_model()


class PostsModelsTest(TestCase):
    '''Testing posts app models.'''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # creating test user for testing
        cls.user = User.objects.create_user(username='test_user')

        # creating test group for testing in Group model
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

        # creating test post for testing in Post model
        cls.post = Post.objects.create(
            text='тестовыйтекст' * 50,
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        '''Preparation before the testing.'''
        self.post = PostsModelsTest.post

    def test_models_have_correct_object_names(self):
        '''Testing __str__ method in Post and Group models.'''
        group = PostsModelsTest.group

        expected_str_post = self.post.text[:15]
        expected_str_group = group.title

        self.assertEqual(expected_str_post, str(self.post))
        self.assertEqual(expected_str_group, str(group))

    def test_verbose_name_in_post_model(self):
        '''Testing verbose_name in Post model
        for educational purposes
        '''

        verbose_field = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }

        for field, value in verbose_field.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, value)

    def test_help_text_in_post_model(self):
        '''Testing help_text in Post model
        for educational purposes
        '''

        help_field = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }

        for field, value in help_field.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text, value)
