from datetime import timedelta
from django.utils import timezone

def calculate_popularity_score(book):
    total_loans = book.instances.filter(loan__isnull=False).count()
    total_reviews = book.reviews.count()
    avg_rating = float(book.average_rating)
    
    loan_weight = 2.0
    review_weight = 1.5
    rating_weight = 10.0
    
    score = (total_loans * loan_weight) + (total_reviews * review_weight) + (avg_rating * rating_weight)
    
    return score

def calculate_fine_amount(loan, policy):
    if not loan.is_overdue():
        return 0
    
    days_overdue = loan.days_overdue()
    fine_amount = days_overdue * float(policy.fine_per_day)
    
    return min(fine_amount, float(policy.max_fine_amount))

def get_available_books_count(book):
    return book.instances.filter(status='AVAILABLE').count()

def can_checkout_book(member, book_instance):
    from circulation.models import Loan, CheckoutPolicy
    
    active_loans = Loan.objects.filter(
        member=member,
        status='ACTIVE'
    ).count()
    
    policy = CheckoutPolicy.objects.filter(
        membership_type=member.membership_type
    ).first()
    
    if not policy:
        return False, "No checkout policy found for membership type"
    
    if active_loans >= policy.max_books:
        return False, f"Maximum books limit ({policy.max_books}) reached"
    
    if book_instance.status != 'AVAILABLE':
        return False, "Book is not available"
    
    if member.status != 'ACTIVE':
        return False, "Member account is not active"
    
    return True, "OK"

def can_renew_loan(loan):
    if loan.status != 'ACTIVE':
        return False, "Loan is not active"
    
    if loan.is_overdue():
        return False, "Cannot renew overdue loan"
    
    if loan.renewal_count >= loan.max_renewals:
        return False, "Maximum renewals reached"
    
    return True, "OK"

def generate_member_id(user_id):
    return f"MEM{user_id:06d}"

def generate_book_barcode(book_id, instance_number):
    return f"BK{book_id:06d}-{instance_number:03d}"
