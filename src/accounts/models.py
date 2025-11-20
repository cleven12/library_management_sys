from django.db import models
from django.contrib.auth.models import User

class MemberProfile(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    member_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    membership_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member_id} - {self.user.get_full_name() or self.user.username}"
    
    class Meta:
        ordering = ['-membership_date']
