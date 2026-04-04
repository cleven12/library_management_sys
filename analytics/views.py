from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import BookPopularity, MemberActivity, LibraryStatistics
from catalog.models import Book
from circulation.models import Loan, Fine
from accounts.models import MemberProfile

def is_librarian(user):
    return hasattr(user, 'librarian_profile')

@login_required
@user_passes_test(is_librarian)
def dashboard(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    total_books = Book.objects.count()
    total_members = MemberProfile.objects.filter(status='ACTIVE').count()
    active_loans = Loan.objects.filter(status='ACTIVE').count()
    overdue_loans = Loan.objects.filter(
        status='ACTIVE',
        due_date__lt=today
    ).count()
    
    recent_checkouts = Loan.objects.filter(
        checkout_date__gte=week_ago
    ).count()
    
    pending_fines = Fine.objects.filter(
        status='PENDING'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'total_books': total_books,
        'total_members': total_members,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
        'recent_checkouts': recent_checkouts,
        'pending_fines': pending_fines,
    }
    return render(request, 'analytics/dashboard.html', context)

@login_required
@user_passes_test(is_librarian)
def popular_books_report(request):
    popular_books = BookPopularity.objects.select_related(
        'book'
    ).order_by('-popularity_score')[:50]
    
    return render(request, 'analytics/popular_books.html', {
        'popular_books': popular_books
    })

@login_required
@user_passes_test(is_librarian)
def member_analytics(request):
    top_borrowers = MemberActivity.objects.select_related(
        'member__user'
    ).order_by('-total_books_borrowed')[:20]
    
    members_with_overdue = MemberActivity.objects.filter(
        total_overdue__gt=0
    ).count()
    
    context = {
        'top_borrowers': top_borrowers,
        'members_with_overdue': members_with_overdue,
    }
    return render(request, 'analytics/member_analytics.html', context)

@login_required
@user_passes_test(is_librarian)
def statistics_report(request):
    last_30_days = [
        timezone.now().date() - timedelta(days=i) 
        for i in range(30)
    ]
    
    stats = LibraryStatistics.objects.filter(
        date__in=last_30_days
    ).order_by('-date')
    
    return render(request, 'analytics/statistics.html', {
        'statistics': stats
    })

@login_required
def my_reading_stats(request):
    profile = MemberProfile.objects.get(user=request.user)
    activity, created = MemberActivity.objects.get_or_create(member=profile)
    
    recent_loans = Loan.objects.filter(
        member=profile
    ).select_related('book_instance__book')[:10]
    
    context = {
        'activity': activity,
        'recent_loans': recent_loans,
    }
    return render(request, 'analytics/my_stats.html', context)
