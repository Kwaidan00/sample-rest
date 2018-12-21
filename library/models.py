from django.db import models


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey('library.Author', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.title)
