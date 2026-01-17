from django.contrib import admin
from .models import Loan, Reservation, Fine, RenewalHistory, CheckoutPolicy

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book_instance', 'member', 'checkout_date', 'due_date', 'status', 'renewal_count']
    list_filter = ['status', 'checkout_date', 'due_date']
    search_fields = ['book_instance__book__title', 'member__user__username', 'member__member_id']
    date_hierarchy = 'checkout_date'
    readonly_fields = ['checkout_date']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'reservation_date', 'status', 'position_in_queue', 'notified']
    list_filter = ['status', 'notified', 'reservation_date']
    search_fields = ['book__title', 'member__user__username']
    date_hierarchy = 'reservation_date'

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'reason', 'status', 'issued_date', 'paid_date']
    list_filter = ['status', 'reason', 'issued_date']
    search_fields = ['member__user__username', 'member__member_id', 'transaction_id']
    date_hierarchy = 'issued_date'

@admin.register(RenewalHistory)
class RenewalHistoryAdmin(admin.ModelAdmin):
    list_display = ['loan', 'renewed_on', 'old_due_date', 'new_due_date', 'renewed_by']
    list_filter = ['renewed_on']
    search_fields = ['loan__book_instance__book__title', 'renewed_by__username']
    date_hierarchy = 'renewed_on'
    readonly_fields = ['renewed_on']

@admin.register(CheckoutPolicy)
class CheckoutPolicyAdmin(admin.ModelAdmin):
    list_display = ['membership_type', 'max_books', 'loan_period_days', 'max_renewals', 'fine_per_day']
    search_fields = ['membership_type']
