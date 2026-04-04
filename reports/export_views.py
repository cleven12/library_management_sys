import csv
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from circulation.models import Loan, Fine
from accounts.models import MemberProfile
from catalog.models import Book

def is_librarian(user):
    return hasattr(user, 'librarian_profile')

@login_required
@user_passes_test(is_librarian)
def export_loans_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="loans_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Member ID', 'Member Name', 'Book Title', 'ISBN', 'Checkout Date', 'Due Date', 'Status'])
    
    loans = Loan.objects.select_related(
        'member__user', 
        'book_instance__book'
    ).filter(status__in=['ACTIVE', 'OVERDUE'])
    
    for loan in loans:
        writer.writerow([
            loan.member.member_id,
            loan.member.user.get_full_name(),
            loan.book_instance.book.title,
            loan.book_instance.book.isbn,
            loan.checkout_date.strftime('%Y-%m-%d'),
            loan.due_date.strftime('%Y-%m-%d'),
            loan.status
        ])
    
    return response

@login_required
@user_passes_test(is_librarian)
def export_members_json(request):
    members = MemberProfile.objects.select_related('user').filter(status='ACTIVE')
    
    data = []
    for member in members:
        data.append({
            'member_id': member.member_id,
            'name': member.user.get_full_name(),
            'email': member.user.email,
            'membership_type': member.membership_type,
            'status': member.status,
            'join_date': member.membership_start.isoformat(),
        })
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="members_export.json"'
    
    return response

@login_required
@user_passes_test(is_librarian)
def export_catalog_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="catalog_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ISBN', 'Title', 'Authors', 'Publisher', 'Publication Date', 'Total Copies', 'Available'])
    
    books = Book.objects.prefetch_related('authors', 'instances').all()
    
    for book in books:
        authors = ', '.join([f"{a.first_name} {a.last_name}" for a in book.authors.all()])
        total_copies = book.instances.count()
        available = book.instances.filter(status='AVAILABLE').count()
        
        writer.writerow([
            book.isbn,
            book.title,
            authors,
            book.publisher.name if book.publisher else '',
            book.publication_date.strftime('%Y-%m-%d'),
            total_copies,
            available
        ])
    
    return response
