from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from catalog.models import Book, BookInstance
from circulation.models import Loan
from datetime import date, timedelta

@staff_member_required
def dashboard(request):
    total_books = Book.objects.count()
    total_copies = BookInstance.objects.count()
    available_copies = BookInstance.objects.filter(status='available').count()
    on_loan_copies = BookInstance.objects.filter(status='on_loan').count()
    
    active_loans = Loan.objects.filter(return_date__isnull=True).count()
    overdue_loans = Loan.objects.filter(
        return_date__isnull=True,
        due_date__lt=date.today()
    ).count()
    
    total_fines = sum(
        loan.fine_amount for loan in Loan.objects.filter(fine_paid=False)
    )
    
    context = {
        'total_books': total_books,
        'total_copies': total_copies,
        'available_copies': available_copies,
        'on_loan_copies': on_loan_copies,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
        'total_fines': total_fines,
    }
    
    return render(request, 'reports/dashboard.html', context=context)

@staff_member_required
def most_borrowed_books(request):
    books_with_loan_count = Book.objects.annotate(
        loan_count=Count('bookinstance__loan')
    ).order_by('-loan_count')[:20]
    
    context = {
        'books': books_with_loan_count,
    }
    
    return render(request, 'reports/most_borrowed.html', context=context)

@staff_member_required
def circulation_statistics(request):
    today = date.today()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    
    loans_last_30_days = Loan.objects.filter(borrow_date__gte=last_30_days).count()
    loans_last_7_days = Loan.objects.filter(borrow_date__gte=last_7_days).count()
    
    returns_last_30_days = Loan.objects.filter(
        return_date__gte=last_30_days,
        return_date__isnull=False
    ).count()
    
    overdue_items = Loan.objects.filter(
        return_date__isnull=True,
        due_date__lt=today
    ).select_related('book_instance__book', 'borrower')
    
    context = {
        'loans_last_30_days': loans_last_30_days,
        'loans_last_7_days': loans_last_7_days,
        'returns_last_30_days': returns_last_30_days,
        'overdue_items': overdue_items,
        'today': today,
    }
    
    return render(request, 'reports/circulation_stats.html', context=context)
