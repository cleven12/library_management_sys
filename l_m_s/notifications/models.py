from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('DUE_SOON', 'Due Soon'),
        ('OVERDUE', 'Overdue'),
        ('RESERVED_AVAILABLE', 'Reserved Book Available'),
        ('FINE_ISSUED', 'Fine Issued'),
        ('MEMBERSHIP_EXPIRY', 'Membership Expiring'),
        ('NEW_BOOK', 'New Book Added'),
        ('REMINDER', 'Reminder'),
        ('ANNOUNCEMENT', 'Announcement'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('READ', 'Read'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.IntegerField(default=1)
    sent_via_email = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['notification_type']),
        ]
        
    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.title}"

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    due_date_reminder = models.BooleanField(default=True)
    overdue_notice = models.BooleanField(default=True)
    reservation_alert = models.BooleanField(default=True)
    new_books_alert = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} Preferences"

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    notification_type = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
