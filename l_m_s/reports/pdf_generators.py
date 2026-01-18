from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
from circulation.models import Loan
from accounts.models import MemberProfile
from datetime import datetime

def is_librarian(user):
    return hasattr(user, 'librarian_profile')

@login_required
@user_passes_test(is_librarian)
def generate_loan_report_pdf(request):
    """Generate PDF report of active loans"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph("Active Loans Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    subtitle = Paragraph(
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    )
    elements.append(subtitle)
    elements.append(Spacer(1, 20))
    
    loans = Loan.objects.filter(
        status='ACTIVE'
    ).select_related('book_instance__book', 'member__user')
    
    data = [['Member', 'Book Title', 'Checkout Date', 'Due Date', 'Status']]
    
    for loan in loans:
        data.append([
            loan.member.user.get_full_name(),
            loan.book_instance.book.title[:40],
            loan.checkout_date.strftime('%Y-%m-%d'),
            loan.due_date.strftime('%Y-%m-%d'),
            'Overdue' if loan.is_overdue() else 'Active'
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="loans_report_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response

@login_required
def generate_member_card_pdf(request):
    """Generate member ID card PDF"""
    profile = MemberProfile.objects.get(user=request.user)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=(300, 180))
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph("Library Member Card", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 10))
    
    info = [
        ['Name:', request.user.get_full_name()],
        ['Member ID:', profile.member_id],
        ['Membership:', profile.get_membership_type_display()],
        ['Valid Until:', profile.membership_end.strftime('%Y-%m-%d') if profile.membership_end else 'N/A']
    ]
    
    table = Table(info)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="member_card_{profile.member_id}.pdf"'
    
    return response
