from django.db import models
from django.urls import reverse

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    biography = models.TextField(blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text='Enter a book genre (e.g. Science Fiction)')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, help_text='Select author(s) for this book')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character ISBN number')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    cover_image = models.URLField(blank=True, help_text='URL to book cover image')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    def display_author(self):
        return ', '.join(author.__str__() for author in self.author.all()[:3])
    
    display_genre.short_description = 'Genre'
    display_author.short_description = 'Author'
    
    class Meta:
        ordering = ['title']

class BookInstance(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_loan', 'On Loan'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True, help_text='Unique ID for this particular book copy')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200, blank=True)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='maintenance', help_text='Book availability')
    
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)
    
    def __str__(self):
        return f'{self.id} ({self.book.title})'
