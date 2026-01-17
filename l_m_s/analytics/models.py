from django.db import models
from django.contrib.auth.models import User

class BookPopularity(models.Model):
    book = models.OneToOneField('catalog.Book', on_delete=models.CASCADE, related_name='popularity')
    total_loans = models.IntegerField(default=0)
    total_reservations = models.IntegerField(default=0)
    total_reviews = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    views_count = models.IntegerField(default=0)
    last_borrowed = models.DateTimeField(null=True, blank=True)
    popularity_score = models.FloatField(default=0.0)
    trending_rank = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity_score']
        verbose_name_plural = 'Book Popularities'
        
    def __str__(self):
        return f"{self.book.title} - Score: {self.popularity_score}"

class MemberActivity(models.Model):
    member = models.OneToOneField('accounts.MemberProfile', on_delete=models.CASCADE, related_name='activity')
    total_books_borrowed = models.IntegerField(default=0)
    total_books_returned = models.IntegerField(default=0)
    total_overdue = models.IntegerField(default=0)
    total_fines_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_reviews_written = models.IntegerField(default=0)
    favorite_genres = models.CharField(max_length=300, blank=True)
    reading_streak_days = models.IntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.member.user.username} Activity"

class LibraryStatistics(models.Model):
    date = models.DateField(unique=True, db_index=True)
    total_members = models.IntegerField(default=0)
    active_members = models.IntegerField(default=0)
    total_books = models.IntegerField(default=0)
    available_books = models.IntegerField(default=0)
    books_on_loan = models.IntegerField(default=0)
    new_members = models.IntegerField(default=0)
    new_loans = models.IntegerField(default=0)
    books_returned = models.IntegerField(default=0)
    overdue_books = models.IntegerField(default=0)
    fines_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    new_books_added = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Library Statistics'
        
    def __str__(self):
        return f"Stats for {self.date}"

class SearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    search_query = models.CharField(max_length=300)
    results_count = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.search_query} - {self.timestamp}"
