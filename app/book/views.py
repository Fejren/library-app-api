from django.shortcuts import render

from core.models import Book, Author, Genre, PublishingHouse
from book import serializers
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BaseBookAttrViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # return assigned objects
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(book__isnull=False)

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(BaseBookAttrViewSet):
    # Manage genres in db
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class AuthorViewSet(BaseBookAttrViewSet):
    # Manage authors in db
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class PublishingHouseViewSet(BaseBookAttrViewSet):
    # Manage publishing houses in db
    queryset = PublishingHouse.objects.all()
    serializer_class = serializers.PublishingHouseSerializer


class BookViewSet(viewsets.ModelViewSet):
    # Manage books in db
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        # convert list of ids to a list of int
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        # Retrieve books for the auth user
        genre = self.request.query_params.get('genre')
        author = self.request.query_params.get('author')
        publi_house = self.request.query_params.get('publishing_house')

        queryset = self.queryset

        if genre:
            genre_ids = self._params_to_ints(genre)
            queryset = queryset.filter(genre__id__in=genre_ids)
        if author:
            author_ids = self._params_to_ints(author)
            queryset = queryset.filter(author__id__in=author_ids)
        if publi_house:
            publi_house_ids = self._params_to_ints(publi_house)
            queryset = queryset.filter(publi_house__id__in=publi_house_ids)

        return queryset

    def get_serializer_class(self):
        # Return appropirate serializer class
        if self.action == 'retrieve':
            return serializers.BookDetailSerializer
        elif self.action == 'upload_image':
            return serializers.BookImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        # Create new book
        serializer.save()

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        # Upload an image to book cover
        book = self.get_object()
        serializer = self.get_serializer(
            book,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
