from django.contrib import admin
from .models import Book, BookInstance, Author, Genre, Language


#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'display_genre', 'language']


#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    fields = ('first_name', 'last_name', ('date_of_birth', 'date_of_death'))


admin.site.register(Genre)

#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ['book', 'status', 'borrower', 'due_back', 'id']
    list_filter = ('status', 'due_back', 'imprint')
    fieldsets = (
        ('Book Info', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Available', {'fields': ('status', 'due_back', 'borrower')})
    )


admin.site.register(Language)
