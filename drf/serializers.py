from rest_framework import serializers

from library.models import Author, Book


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    book_set = serializers.HyperlinkedRelatedField(many=True, view_name='drf:book-detail', read_only=True)

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'book_set')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author_url = serializers.HyperlinkedIdentityField(view_name="drf:author-detail")

    class Meta:
        model = Book
        fields = ('title', 'author_url')
