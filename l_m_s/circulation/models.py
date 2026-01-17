from django.db import models
from django.utils import timezone
from datetime import timedelta
from catalog.models import BookInstance
from accounts.models import MemberProfile

class Loan(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
        ('LOST', 'Lost'),
    ]
    
    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE)
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='loans')
    checkout_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateTimeField(null=True, blank=True)
    renewal_count = models.IntegerField(default=0)
    max_renewals = models.IntegerField(default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    checked_out_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='loans_processed')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-checkout_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]
        
    def __str__(self):
        return f"{self.book_instance.book.title} - {self.member.user.username}"
    
    def is_overdue(self):
        if self.status == 'RETURNED':
            return False
        return timezone.now().date() > self.due_date
    
    def days_overdue(self):
        if not self.is_overdue():
            return 0
        return (timezone.now().date() - self.due_date).days

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('FULFILLED', 'Fulfilled'),
        ('CANCELLED', 'Cancelled'),
        ('EXPIRED', 'Expired'),
    ]
    
    book = models.ForeignKey('catalog.Book', on_delete=models.CASCADE)
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    position_in_queue = models.IntegerField(default=1)
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['reservation_date']
        
    def __str__(self):
        return f"{self.book.title} - {self.member.user.username}"

class Fine(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('WAIVED', 'Waived'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    REASON_CHOICES = [
        ('OVERDUE', 'Overdue Book'),
        ('DAMAGE', 'Damaged Book'),
        ('LOST', 'Lost Book'),
        ('OTHER', 'Other'),
    ]
    
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='fines')
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    issued_date = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-issued_date']
        
    def __str__(self):
        return f"{self.member.user.username} - ${self.amount} - {self.reason}"

class RenewalHistory(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='renewal_history')
    renewed_on = models.DateTimeField(auto_now_add=True)
    old_due_date = models.DateField()
    new_due_date = models.DateField()
    renewed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-renewed_on']
        
    def __str__(self):
        return f"{self.loan} - Renewed on {self.renewed_on}"

class CheckoutPolicy(models.Model):
    membership_type = models.CharField(max_length=20, unique=True)
    max_books = models.IntegerField(default=5)
    loan_period_days = models.IntegerField(default=14)
    max_renewals = models.IntegerField(default=3)
    fine_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=0.50)
    max_fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    
    def __str__(self):
        return f"{self.membership_type} Policy"
