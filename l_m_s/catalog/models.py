from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Book(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('ES', 'Spanish'),
        ('FR', 'French'),
        ('DE', 'German'),
        ('ZH', 'Chinese'),
        ('JA', 'Japanese'),
        ('HI', 'Hindi'),
        ('AR', 'Arabic'),
    ]
    
    title = models.CharField(max_length=300, db_index=True)
    subtitle = models.CharField(max_length=300, blank=True)
    authors = models.ManyToManyField(Author, related_name='books')
    isbn = models.CharField('ISBN', max_length=13, unique=True, db_index=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField()
    genres = models.ManyToManyField(Genre, related_name='books')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN')
    pages = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_ratings = models.IntegerField(default=0)
    dewey_decimal = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
        ]
        
    def __str__(self):
        return self.title
    
    def get_availability_status(self):
        total = self.instances.count()
        available = self.instances.filter(status='AVAILABLE').count()
        
        if available == 0:
            return 'unavailable'
        elif available <= total * 0.3:
            return 'limited'
        else:
            return 'available'
    
    def get_next_available_date(self):
        from circulation.models import Loan
        active_loans = Loan.objects.filter(
            book_instance__book=self,
            status='ACTIVE'
        ).order_by('due_date').first()
        
        if active_loans:
            return active_loans.due_date
        return None

class BookInstance(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON_LOAN', 'On Loan'),
        ('RESERVED', 'Reserved'),
        ('MAINTENANCE', 'Maintenance'),
        ('LOST', 'Lost'),
        ('DAMAGED', 'Damaged'),
    ]
    
    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='instances')
    unique_id = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='GOOD')
    acquisition_date = models.DateField(default=timezone.now)
    acquisition_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['book', 'unique_id']
        
    def __str__(self):
        return f"{self.book.title} ({self.unique_id})"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'user']
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class ReadingList(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    books = models.ManyToManyField(Book, related_name='reading_lists')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
