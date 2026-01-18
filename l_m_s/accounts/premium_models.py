from django.db import models
from accounts.models import MemberProfile
from django.utils import timezone

class MembershipPlan(models.Model):
    PLAN_TYPES = [
        ('FREE', 'Free'),
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    max_books = models.IntegerField()
    max_ebooks = models.IntegerField(default=0)
    priority_support = models.BooleanField(default=False)
    early_access = models.BooleanField(default=False)
    features = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    ]
    
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.plan.name}"
    
    def is_active(self):
        return self.status == 'ACTIVE' and timezone.now().date() <= self.end_date

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CARD', 'Credit/Debit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK', 'Bank Transfer'),
        ('CASH', 'Cash'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=200, unique=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.member.user.username} - ${self.amount}"

class Wishlist(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='wishlists')
    book = models.ForeignKey('catalog.Book', on_delete=models.CASCADE)
    priority = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    notify_on_available = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['member', 'book']
        ordering = ['-priority', '-added_at']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.book.title}"

class Badge(models.Model):
    BADGE_CATEGORIES = [
        ('READING', 'Reading Achievement'),
        ('PARTICIPATION', 'Participation'),
        ('MILESTONE', 'Milestone'),
        ('SPECIAL', 'Special Event'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=BADGE_CATEGORIES)
    icon = models.ImageField(upload_to='badges/', null=True, blank=True)
    requirement = models.JSONField()
    points = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class MemberBadge(models.Model):
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['member', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.badge.name}"
