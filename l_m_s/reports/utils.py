import csv
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta

def export_loans_to_csv(loans):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="loans_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Loan ID', 'Member', 'Book Title', 'Checkout Date', 'Due Date', 'Status', 'Renewal Count'])
    
    for loan in loans:
        writer.writerow([
            loan.id,
            loan.member.user.username,
            loan.book_instance.book.title,
            loan.checkout_date.strftime('%Y-%m-%d'),
            loan.due_date.strftime('%Y-%m-%d'),
            loan.status,
            loan.renewal_count
        ])
    
    return response

def export_members_to_csv(members):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="members_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Member ID', 'Name', 'Email', 'Membership Type', 'Status', 'Join Date'])
    
    for member in members:
        writer.writerow([
            member.member_id,
            member.user.get_full_name(),
            member.user.email,
            member.membership_type,
            member.status,
            member.membership_start.strftime('%Y-%m-%d')
        ])
    
    return response

def export_fines_to_csv(fines):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="fines_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Fine ID', 'Member', 'Amount', 'Reason', 'Status', 'Issued Date', 'Paid Date'])
    
    for fine in fines:
        writer.writerow([
            fine.id,
            fine.member.user.username,
            f'${fine.amount}',
            fine.reason,
            fine.status,
            fine.issued_date.strftime('%Y-%m-%d'),
            fine.paid_date.strftime('%Y-%m-%d') if fine.paid_date else 'N/A'
        ])
    
    return response
