from django.db import models

class APIKey(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.key[:10]}..."

class WebhookEvent(models.Model):
    EVENT_TYPES = [
        ('BOOK_CHECKOUT', 'Book Checkout'),
        ('BOOK_RETURN', 'Book Return'),
        ('FINE_PAID', 'Fine Paid'),
        ('MEMBER_REGISTERED', 'Member Registered'),
    ]
    
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    payload = models.JSONField()
    url = models.URLField()
    status_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
