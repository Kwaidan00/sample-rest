from rest_framework import generics, permissions

from rest_framework.generics import get_object_or_404

from drf import serializers
from library.models import Book, Author, PersonalLibrary


class IsTheOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user_id = view.kwargs['user_pk']
        return (
                request.method in permissions.SAFE_METHODS or
                (request.user and request.user.is_authenticated and request.user.id == user_id)
        )


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


class PersonalLibraryDetail(generics.RetrieveAPIView):
    queryset = PersonalLibrary.objects.all()
    serializer_class = serializers.PersonalLibrarySerializer
    permission_classes = (IsTheOwnerOrReadOnly,)

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs['user_pk']
        obj = get_object_or_404(queryset, user_id=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class PersonalLibraryBooksList(generics.ListCreateAPIView):
    serializer_class = serializers.PersonalLibraryBookSerializer
    permission_classes = (IsTheOwnerOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs['user_pk']
        library = get_object_or_404(PersonalLibrary, user_id=pk)
        return library.books.all()

    def perform_create(self, serializer):
        book = serializer.save(user=self.request.user)


class PersonalLibraryBookDetail(generics.RetrieveDestroyAPIView):
    queryset = PersonalLibrary.objects.all()
    serializer_class = serializers.PersonalLibraryBookSerializer
    permission_classes = (IsTheOwnerOrReadOnly,)

    def get_object(self):
        queryset = self.get_queryset()
        user_pk = self.kwargs['user_pk']
        pk = self.kwargs['pk']
        obj = get_object_or_404(queryset, user_id=user_pk)
        self.check_object_permissions(self.request, obj)
        book = get_object_or_404(obj.books.all(), pk=pk)
        return book

    def perform_destroy(self, instance):
        user_pk = self.kwargs['user_pk']
        queryset = self.get_queryset()
        library = get_object_or_404(queryset, user_id=user_pk)
        library.books.remove(instance)
