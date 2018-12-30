from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from library.models import Author, Book, PersonalLibrary


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    book_set = serializers.HyperlinkedRelatedField(many=True, view_name='drf:book-detail', read_only=True)

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'book_set')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(view_name="drf:author-detail", lookup_field='pk',
                                                 queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ('id', 'title', 'author')


class PersonalLibrarySerializer(serializers.HyperlinkedModelSerializer):
    books_url = serializers.HyperlinkedIdentityField(view_name='drf:library-detail-books-list',
                                                     lookup_field='user_id',
                                                     lookup_url_kwarg='user_pk')

    class Meta:
        model = PersonalLibrary
        fields = ('user_id', 'books_url')


class PersonalLibraryBookSerializer(BookSerializer):
    id = serializers.IntegerField(read_only=False)

    def create(self, validated_data):
        user = validated_data.pop('user')
        book_pk = validated_data.pop('id')
        book_title = validated_data.pop('title')
        book_author = validated_data.pop('author')
        book = get_object_or_404(Book, pk=book_pk)
        library = PersonalLibrary.objects.get(user=user)
        library.books.add(book)
        return book

