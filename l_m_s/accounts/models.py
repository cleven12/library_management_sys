from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class MemberProfile(models.Model):
    MEMBERSHIP_TYPES = [
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium'),
        ('VIP', 'VIP'),
        ('STUDENT', 'Student'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('EXPIRED', 'Expired'),
        ('PENDING', 'Pending'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    member_id = models.CharField(max_length=20, unique=True, db_index=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default='STANDARD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    membership_start = models.DateField(auto_now_add=True)
    membership_end = models.DateField(null=True, blank=True)
    max_books_allowed = models.IntegerField(default=5)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    preferred_genres = models.CharField(max_length=200, blank=True)
    notification_preference = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['member_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.member_id}"

class LibrarianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='librarian_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=17)
    access_level = models.IntegerField(default=1)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    details = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
