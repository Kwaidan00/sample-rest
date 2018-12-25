from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey('library.Author', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'
        ordering = ['title']

    def __str__(self):
        return '{}'.format(self.title)


class PersonalLibrary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField('library.Book', related_name='in_library')

    class Meta:
        verbose_name = 'personal library'
        verbose_name_plural = 'personal libraries'
        ordering = ['user']

    def __str__(self):
        return '{}\'s library'.format(self.user.username)
