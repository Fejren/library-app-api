import os
import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from isbn_field import ISBNField


class TimeStampedMixin(models.Model):
    # Abstract model that defines the auto populated 'created_date' and
    # 'last_modified' fields.
    # This model must be used as the base for all the models in the project.

    created_date = models.DateTimeField(
        editable=False,
        blank=True, null=True,
        auto_now_add=True,
        verbose_name=_('created date')
    )
    last_modified = models.DateTimeField(
        editable=False,
        blank=True, null=True,
        auto_now=True,
        verbose_name=_('last modified'),
    )

    class Meta:

        abstract = True


class CatalogueMixin(TimeStampedMixin):
    # Abstract model that defines name, is active and extends
    # from TimeStampedMixin.
    # This model must be used as the base for catalogue models in the project.

    name = models.CharField(
        max_length=255,
        verbose_name='name'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='is active'
    )
    was_deleted = models.BooleanField(
        default=False,
        verbose_name='was deleted'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


def cover_image_file_path(instance, filename):
    # Generate file path for new cover image
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('upload/cover/', filename)


class Author(TimeStampedMixin):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PublishingHouse(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Genre(CatalogueMixin):
    # Genre to be used for a book

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Book(CatalogueMixin):
    # Model of a book, but not a specific book

    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE)
    publishing_house = models.ForeignKey(PublishingHouse,
                                         on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000)
    num_of_pages = models.IntegerField()
    isbn = ISBNField(unique=True)
    year_of_publish = models.DateField()
    cover = models.ImageField(null=True, upload_to=cover_image_file_path)
    genre = models.ManyToManyField(
        Genre,
        related_name='books',
        related_query_name='book',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    # Model for a specific copy of a book,
    # this will be useful for borrowing system

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='books',
        related_query_name='book'
    )
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )
    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, blank=True, default='a'
    )

    class Meta:
        verbose_name = _('book instance')
        verbose_name_plural = _('book instances')

    def __str__(self):
        return f'{self.id} {self.book.name}'


class UserManager(BaseUserManager):

    def create_user(self, name, email, password=None, **extra_fields):
        # Create and save new user
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have name')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, name, email, password):
        # Create new superuser
        user = self.create_user(name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Custom user model, supports email instead of username

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

