from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from circulation.models import Loan, Fine, CheckoutPolicy
from notifications.utils import send_due_date_reminder, send_overdue_notice

@shared_task
def send_due_date_reminders():
    today = timezone.now().date()
    reminder_date = today + timedelta(days=3)
    
    loans = Loan.objects.filter(
        status='ACTIVE',
        due_date=reminder_date
    ).select_related('member__user', 'book_instance__book')
    
    count = 0
    for loan in loans:
        send_due_date_reminder(loan)
        count += 1
    
    return f'Sent {count} reminders'

@shared_task
def process_overdue_loans():
    today = timezone.now().date()
    
    overdue_loans = Loan.objects.filter(
        status='ACTIVE',
        due_date__lt=today
    ).select_related('member', 'book_instance__book')
    
    for loan in overdue_loans:
        loan.status = 'OVERDUE'
        loan.save()
        
        send_overdue_notice(loan)
        
        existing_fine = Fine.objects.filter(
            loan=loan,
            reason='OVERDUE'
        ).first()
        
        if not existing_fine:
            policy = CheckoutPolicy.objects.filter(
                membership_type=loan.member.membership_type
            ).first()
            
            if policy:
                days_overdue = (today - loan.due_date).days
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
    
    return f'Processed {overdue_loans.count()} overdue loans'

@shared_task
def update_book_popularity():
    from analytics.models import BookPopularity
    from catalog.models import Book
    
    for book in Book.objects.all():
        total_loans = book.instances.filter(loan__isnull=False).count()
        total_reviews = book.reviews.count()
        avg_rating = float(book.average_rating)
        
        popularity_score = (total_loans * 2) + (total_reviews * 1.5) + (avg_rating * 10)
        
        BookPopularity.objects.update_or_create(
            book=book,
            defaults={
                'total_loans': total_loans,
                'total_reviews': total_reviews,
                'average_rating': avg_rating,
                'popularity_score': popularity_score,
            }
        )
    
    return 'Updated book popularity'

@shared_task
def cleanup_old_notifications():
    from notifications.models import Notification
    
    cutoff_date = timezone.now() - timedelta(days=90)
    
    deleted = Notification.objects.filter(
        created_at__lt=cutoff_date,
        status='READ'
    ).delete()
    
    return f'Deleted {deleted[0]} old notifications'
