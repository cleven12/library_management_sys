from django.db import models
from django.contrib.auth.models import User
from catalog.models import BookInstance, Book
from datetime import date, timedelta

class Loan(models.Model):
    book_instance = models.ForeignKey(BookInstance, on_delete=models.RESTRICT)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    fine_paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-borrow_date']
        permissions = (("can_manage_loans", "Can manage all loans"),)
    
    def __str__(self):
        return f'{self.book_instance.book.title} - {self.borrower.username if self.borrower else "Unknown"}'
    
    @property
    def is_overdue(self):
        if self.return_date:
            return False
        return date.today() > self.due_date
    
    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (date.today() - self.due_date).days
    
    def calculate_fine(self, rate_per_day=0.50):
        if self.is_overdue:
            self.fine_amount = self.days_overdue * rate_per_day
            self.save()
        return self.fine_amount
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=14)
        super().save(*args, **kwargs)

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ready', 'Ready for Pickup'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    expiry_date = models.DateField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['reservation_date']
        unique_together = [['book', 'member', 'status']]
    
    def __str__(self):
        return f'{self.book.title} - {self.member.username} ({self.status})'
    
    def save(self, *args, **kwargs):
        if not self.expiry_date and self.status == 'ready':
            self.expiry_date = date.today() + timedelta(days=3)
        super().save(*args, **kwargs)
