from rest_framework import generics, permissions

# Create your views here.
from drf import serializers
from library.models import Book, Author


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
