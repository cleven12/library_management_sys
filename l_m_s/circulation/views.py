from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Loan, Reservation, Fine, RenewalHistory, CheckoutPolicy
from catalog.models import BookInstance
from accounts.models import MemberProfile, ActivityLog

def is_librarian(user):
    return hasattr(user, 'librarian_profile')

@login_required
def my_loans(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    active_loans = Loan.objects.filter(
        member=profile,
        status__in=['ACTIVE', 'OVERDUE']
    ).select_related('book_instance__book')
    
    loan_history = Loan.objects.filter(
        member=profile,
        status='RETURNED'
    ).select_related('book_instance__book')[:20]
    
    context = {
        'active_loans': active_loans,
        'loan_history': loan_history,
    }
    return render(request, 'circulation/my_loans.html', context)

@login_required
@user_passes_test(is_librarian)
def checkout_book(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        instance_id = request.POST.get('instance_id')
        
        member = get_object_or_404(MemberProfile, member_id=member_id)
        instance = get_object_or_404(BookInstance, unique_id=instance_id)
        
        policy = CheckoutPolicy.objects.filter(
            membership_type=member.membership_type
        ).first()
        
        if not policy:
            policy = CheckoutPolicy.objects.create(
                membership_type=member.membership_type,
                max_books=5,
                loan_period_days=14
            )
        
        active_loans_count = Loan.objects.filter(
            member=member,
            status='ACTIVE'
        ).count()
        
        if active_loans_count >= policy.max_books:
            return render(request, 'circulation/checkout.html', {
                'error': 'Member has reached maximum book limit'
            })
        
        if instance.status != 'AVAILABLE':
            return render(request, 'circulation/checkout.html', {
                'error': 'Book is not available'
            })
        
        due_date = timezone.now().date() + timedelta(days=policy.loan_period_days)
        
        loan = Loan.objects.create(
            book_instance=instance,
            member=member,
            due_date=due_date,
            max_renewals=policy.max_renewals,
            checked_out_by=request.user
        )
        
        instance.status = 'ON_LOAN'
        instance.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='BOOK_CHECKOUT',
            details=f'Checked out {instance.book.title} to {member.user.username}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return redirect('checkout_success', loan_id=loan.id)
    
    return render(request, 'circulation/checkout.html')

@login_required
@user_passes_test(is_librarian)
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    
    loan.return_date = timezone.now()
    loan.status = 'RETURNED'
    loan.save()
    
    loan.book_instance.status = 'AVAILABLE'
    loan.book_instance.save()
    
    if loan.is_overdue():
        days_overdue = loan.days_overdue()
        policy = CheckoutPolicy.objects.filter(
            membership_type=loan.member.membership_type
        ).first()
        
        if policy:
            fine_amount = min(
                days_overdue * float(policy.fine_per_day),
                float(policy.max_fine_amount)
            )
            
            Fine.objects.create(
                member=loan.member,
                loan=loan,
                amount=fine_amount,
                reason='OVERDUE',
                description=f'{days_overdue} days overdue'
            )
    
    ActivityLog.objects.create(
        user=request.user,
        action='BOOK_RETURN',
        details=f'Returned {loan.book_instance.book.title} from {loan.member.user.username}',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    return redirect('loan_detail', loan_id=loan.id)

@login_required
def renew_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    
    if loan.member.user != request.user:
        return redirect('my_loans')
    
    if loan.renewal_count >= loan.max_renewals:
        return render(request, 'circulation/renew_error.html', {
            'error': 'Maximum renewals reached'
        })
    
    if loan.is_overdue():
        return render(request, 'circulation/renew_error.html', {
            'error': 'Cannot renew overdue book'
        })
    
    policy = CheckoutPolicy.objects.filter(
        membership_type=loan.member.membership_type
    ).first()
    
    old_due_date = loan.due_date
    new_due_date = old_due_date + timedelta(days=policy.loan_period_days if policy else 14)
    
    RenewalHistory.objects.create(
        loan=loan,
        old_due_date=old_due_date,
        new_due_date=new_due_date,
        renewed_by=request.user
    )
    
    loan.due_date = new_due_date
    loan.renewal_count += 1
    loan.save()
    
    ActivityLog.objects.create(
        user=request.user,
        action='LOAN_RENEWAL',
        details=f'Renewed loan for {loan.book_instance.book.title}',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    return redirect('my_loans')

@login_required
def my_reservations(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    reservations = Reservation.objects.filter(
        member=profile
    ).select_related('book').order_by('-reservation_date')
    
    return render(request, 'circulation/my_reservations.html', {
        'reservations': reservations
    })

@login_required
def create_reservation(request, book_id):
    from catalog.models import Book
    
    book = get_object_or_404(Book, id=book_id)
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    available_count = book.instances.filter(status='AVAILABLE').count()
    
    if available_count > 0:
        return render(request, 'circulation/reservation_error.html', {
            'error': 'Book is available for checkout'
        })
    
    existing = Reservation.objects.filter(
        book=book,
        member=profile,
        status='ACTIVE'
    ).exists()
    
    if existing:
        return render(request, 'circulation/reservation_error.html', {
            'error': 'You already have an active reservation for this book'
        })
    
    queue_position = Reservation.objects.filter(
        book=book,
        status='ACTIVE'
    ).count() + 1
    
    Reservation.objects.create(
        book=book,
        member=profile,
        expiry_date=timezone.now().date() + timedelta(days=7),
        position_in_queue=queue_position
    )
    
    ActivityLog.objects.create(
        user=request.user,
        action='BOOK_RESERVATION',
        details=f'Reserved {book.title}',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    return redirect('my_reservations')

@login_required
def my_fines(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    fines = Fine.objects.filter(member=profile).order_by('-issued_date')
    
    total_pending = sum(f.amount for f in fines if f.status == 'PENDING')
    
    context = {
        'fines': fines,
        'total_pending': total_pending,
    }
    return render(request, 'circulation/my_fines.html', context)
