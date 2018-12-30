import json

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token

# Create your tests here.
from library.models import Book, Author, PersonalLibrary


class DrfBaseTest(TestCase):
    fixtures = ['test_fixture.json', ]

    def setUp(self):
        self.client = Client()


class SignInBaseTest(DrfBaseTest):
    USERNAME = 'test'
    EMAIL = 'test@example.com'
    PASSWORD = 'password'

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username=self.USERNAME,
                                        email=self.EMAIL, password=self.PASSWORD)
        self.token = Token.objects.create(user=self.user)
        # token.key


class NoSignInTests(DrfBaseTest):

    def test_get_all_books(self):
        response = self.client.get(reverse('drf:books-list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode(encoding='UTF-8'))
        self.assertEqual(data[0]['title'], 'Czysta architektura')

    def test_get_all_authors(self):
        response = self.client.get(reverse('drf:authors-list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode(encoding='UTF-8'))
        self.assertEqual(data[0]['last_name'], 'Martin')


class PersonalLibrarySignedTests(SignInBaseTest):

    def setUp(self):
        super().setUp()
        author = Author.objects.all()[0]
        self.book = Book.objects.all()[0]
        self.new_book = Book.objects.create(title="Agile Software Development",
                                            author=author)
        self.personal_library = PersonalLibrary.objects.create(user=self.user)
        self.personal_library.books.add(self.book)

    def test_get_book_list(self):
        response = self.client.get(
            reverse('drf:library-detail-books-list', kwargs={'user_pk': self.user.pk}),
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode(encoding='UTF-8'))
        self.assertEqual(data[0]['id'], self.book.pk)

    def test_add_book(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token.key
        }
        response = self.client.post(
            reverse('drf:library-detail-books-list', kwargs={'user_pk': self.user.pk}),
            content_type='application/json',
            data=json.dumps({
                'id': self.new_book.id,
                'title': self.new_book.title,
                'author': reverse('drf:author-detail', kwargs={'pk': self.new_book.author.id})
            }),
            **headers
        )
        self.assertEqual(response.status_code, 201)

    def test_add_book_without_token(self):
        response = self.client.post(
            reverse('drf:library-detail-books-list', kwargs={'user_pk': self.user.pk}),
            content_type='application/json',
            data=json.dumps({
                'id': self.new_book.id,
                'title': self.new_book.title,
                'author': reverse('drf:author-detail', kwargs={'pk': self.new_book.author.id})
            }),
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_book(self):
        headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token.key
        }
        response = self.client.delete(
            reverse('drf:library-detail-book-detail', kwargs={'user_pk': self.user.pk,
                                                              'pk': self.book.pk}),
            **headers
        )
        self.assertEqual(response.status_code, 204)
