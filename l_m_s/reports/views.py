from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from circulation.models import Loan, Fine
from catalog.models import Book

def is_librarian(user):
    return hasattr(user, 'librarian_profile')

@login_required
@user_passes_test(is_librarian)
def circulation_report(request):
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    
    total_loans = Loan.objects.filter(
        checkout_date__gte=last_30_days
    ).count()
    
    returned_books = Loan.objects.filter(
        return_date__gte=last_30_days,
        status='RETURNED'
    ).count()
    
    most_borrowed = Book.objects.annotate(
        loan_count=Count('instances__loan')
    ).order_by('-loan_count')[:20]
    
    context = {
        'total_loans': total_loans,
        'returned_books': returned_books,
        'most_borrowed': most_borrowed,
    }
    return render(request, 'reports/circulation.html', context)

@login_required
@user_passes_test(is_librarian)
def overdue_report(request):
    today = timezone.now().date()
    
    overdue_loans = Loan.objects.filter(
        status='ACTIVE',
        due_date__lt=today
    ).select_related('book_instance__book', 'member__user').order_by('due_date')
    
    return render(request, 'reports/overdue.html', {
        'overdue_loans': overdue_loans
    })

@login_required
@user_passes_test(is_librarian)
def revenue_report(request):
    last_30_days = timezone.now().date() - timedelta(days=30)
    
    fines_data = Fine.objects.filter(
        issued_date__gte=last_30_days
    ).values('status').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    total_collected = Fine.objects.filter(
        status='PAID',
        paid_date__gte=last_30_days
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'fines_data': fines_data,
        'total_collected': total_collected,
    }
    return render(request, 'reports/revenue.html', context)
