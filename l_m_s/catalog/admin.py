from django.contrib import admin
from .models import Author, Genre, Publisher, Book, BookInstance, Review, ReadingList

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nationality', 'date_of_birth']
    search_fields = ['first_name', 'last_name', 'nationality']
    list_filter = ['nationality']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'email']
    search_fields = ['name', 'country']
    list_filter = ['country']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'publisher', 'publication_date', 'language', 'average_rating']
    list_filter = ['language', 'publication_date', 'genres']
    search_fields = ['title', 'isbn', 'authors__first_name', 'authors__last_name']
    filter_horizontal = ['authors', 'genres']
    date_hierarchy = 'publication_date'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'book', 'status', 'condition', 'location']
    list_filter = ['status', 'condition', 'acquisition_date']
    search_fields = ['unique_id', 'barcode', 'book__title']
    date_hierarchy = 'acquisition_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at', 'helpful_count']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'user__username']
    filter_horizontal = ['books']
