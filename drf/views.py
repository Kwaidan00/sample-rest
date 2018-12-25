from rest_framework import generics, permissions

# Create your views here.
from drf import serializers
from library.models import Book, Author, PersonalLibrary


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PersonalLibraryDetail(generics.ListCreateAPIView):
    serializer_class = serializers.PersonalLibrarySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        return PersonalLibrary.objects.filter(user_id=pk)

    def perform_create(self, serializer):
        book = serializer.save(user=self.request.user)
