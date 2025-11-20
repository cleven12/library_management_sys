from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death'), 'biography']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'display_genre', 'isbn')
    search_fields = ('title', 'isbn')

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('id', 'book', 'imprint')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
