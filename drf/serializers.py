from rest_framework import serializers

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
    books = serializers.HyperlinkedRelatedField(many=True, view_name='drf:book-detail',
                                                queryset=Book.objects.all())

    class Meta:
        model = PersonalLibrary
        fields = ('books',)

    def create(self, validated_data):
        books = validated_data.pop('books')
        user = validated_data.pop('user')
        library = PersonalLibrary.objects.get(user=user)
        for book in books:
            library.books.add(book)
        return library
