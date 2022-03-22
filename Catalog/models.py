import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=255, help_text="Saisir les genre litteraire disponible(ex: Science fiction)")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Saisir La Langue ex: French, English, Spanish etc..')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True)
    summary = models.TextField(max_length=1000, help_text="Entrer une breve description du livre")
    isbn = models.CharField('ISBN', max_length=13, help_text="Saisir le numero ISBN du livre")
    genre = models.ManyToManyField('Genre', help_text="Saisir le genre litteraire du livre")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Catalog:book-detail", args=[str(self.id)])

    def display_genre(self):
        return ' , '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID pour ce livre particulier')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Livres disponibles'
    )

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse("Catalog:author-detail", args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


