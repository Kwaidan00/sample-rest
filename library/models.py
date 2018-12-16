from django.db import models


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey('library.Author', on_delete=models.CASCADE)
