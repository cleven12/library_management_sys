from django.contrib import admin
from .models import Loan, Reservation

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book_instance', 'borrower', 'borrow_date', 'due_date', 'return_date', 'is_overdue')
    list_filter = ('borrow_date', 'due_date', 'return_date')
    search_fields = ('borrower__username', 'book_instance__book__title')
    fieldsets = (
        (None, {
            'fields': ('book_instance', 'borrower')
        }),
        ('Dates', {
            'fields': ('borrow_date', 'due_date', 'return_date')
        }),
        ('Fines', {
            'fields': ('fine_amount', 'fine_paid')
        }),
    )
    readonly_fields = ('borrow_date',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'reservation_date', 'status', 'expiry_date')
    list_filter = ('status', 'reservation_date')
    search_fields = ('member__username', 'book__title')
