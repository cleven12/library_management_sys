from django.core.validators import FileExtensionValidator
from django.db import models
from catalog.models import Book
from accounts.models import MemberProfile

class BookRecommendation(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='recommendations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-score', '-created_at']
        unique_together = ['member', 'book']
    
    def __str__(self):
        return f"{self.book.title} for {self.member.user.username}"

class ReadingChallenge(models.Model):
    CHALLENGE_TYPES = [
        ('BOOKS_COUNT', 'Number of Books'),
        ('PAGES_COUNT', 'Number of Pages'),
        ('GENRES', 'Different Genres'),
        ('AUTHORS', 'Different Authors'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    target_value = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ChallengeParticipation(models.Model):
    challenge = models.ForeignKey(ReadingChallenge, on_delete=models.CASCADE)
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE)
    current_progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['challenge', 'member']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.challenge.name}"

class BookDiscussion(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=300)
    description = models.TextField()
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.book.title}"

class DiscussionComment(models.Model):
    discussion = models.ForeignKey(BookDiscussion, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} on {self.discussion.title}"

class EBookFile(models.Model):
    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('EPUB', 'EPUB'),
        ('MOBI', 'MOBI'),
        ('TXT', 'Text'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ebook_files')
    file = models.FileField(
        upload_to='ebooks/',
        validators=[FileExtensionValidator(['pdf', 'epub', 'mobi', 'txt'])]
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    file_size = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    downloads_count = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['book', 'format']
    
    def __str__(self):
        return f"{self.book.title} - {self.format}"

class EBookDownload(models.Model):
    ebook = models.ForeignKey(EBookFile, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.ebook.book.title}"
