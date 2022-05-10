from core.models import Author, PublishingHouse, \
    Genre, Book, BookInstance
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    # Serializer for genre objects

    class Meta:
        model = Genre
        fields = ('id', 'name')
        read_only_fields = ('id',)


class AuthorSerializer(serializers.ModelSerializer):
    # Serializer for author
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')
        read_only_fields = ('id',)


class PublishingHouseSerializer(serializers.ModelSerializer):
    # Serializer for publishing house
    class Meta:
        model = PublishingHouse
        fields = ('id', 'name')
        read_only_fields = ('id',)


class BookSerializer(serializers.ModelSerializer):
    # Serializer for book
    publishing_house = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=PublishingHouse.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Author.objects.all()
    )
    genre = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Book
        fields = ('id', 'name', 'author',
                  'publishing_house', 'summary',
                  'number_of_pages', 'isbn',
                  'year_of_publish',
                  'genre')
        read_only_fields = ('id',)


class BookDetailSerializer(BookSerializer):
    # Serializer for a book detail
    publishing_house = PublishingHouseSerializer(many=False, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)


class BookImageSerializer(serializers.ModelSerializer):
    # Serializer for uploading covers to books

    class Meta:
        model = Book
        fields = ('id', 'cover')
        read_only_fields = ('id',)