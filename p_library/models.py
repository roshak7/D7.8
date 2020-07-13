from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

import uuid


class Author(models.Model):
    full_name = models.TextField(verbose_name='Имя')
    birth_year = models.SmallIntegerField(verbose_name='Год рождения')
    country = models.CharField(verbose_name='Страна', max_length=2)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Publisher(models.Model):
    name = models.TextField(verbose_name='Название издательства')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    year_release = models.SmallIntegerField(verbose_name='Год издания')
    copy_count = models.SmallIntegerField(default=0, verbose_name='Кол-во', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена', blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор',
                               related_name='book_author')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_DEFAULT, default=1,
                                  verbose_name='Издатель')
    friend_reader = models.ManyToManyField('p_library.Friend', related_name='book_reader',
                                           verbose_name='Читающие друзья', blank=True)
    image = models.ImageField(upload_to='book_covers', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} ({self.year_release})'


class Friend(models.Model):
    name = models.TextField(verbose_name='Имя друга')
    books = models.ManyToManyField('p_library.Book', related_name='books', blank=True,
                                   through=Book.friend_reader.through,
                                   verbose_name='Книги')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')
    birth_year = models.SmallIntegerField(verbose_name='Год рождения')
    email = models.EmailField(max_length=254)
    location=models.CharField(max_length=120, verbose_name='Локация')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
