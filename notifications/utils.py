from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from notifications.models import EmailTemplate, Notification

def send_notification_email(user, notification_type, context):
    template = EmailTemplate.objects.filter(
        notification_type=notification_type,
        is_active=True
    ).first()
    
    if not template:
        return False
    
    subject = template.subject
    message = template.body.format(**context)
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def create_notification(user, notification_type, title, message, priority=1):
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        priority=priority
    )

def send_due_date_reminder(loan):
    context = {
        'user_name': loan.member.user.get_full_name(),
        'book_title': loan.book_instance.book.title,
        'due_date': loan.due_date.strftime('%Y-%m-%d'),
    }
    
    notification = create_notification(
        user=loan.member.user,
        notification_type='DUE_SOON',
        title=f'Book due soon: {loan.book_instance.book.title}',
        message=f'Your book is due on {loan.due_date}',
        priority=2
    )
    
    if loan.member.notification_preference and loan.member.notification_preference.email_enabled:
        send_notification_email(loan.member.user, 'DUE_SOON', context)
        notification.sent_via_email = True
        notification.save()

def send_overdue_notice(loan):
    context = {
        'user_name': loan.member.user.get_full_name(),
        'book_title': loan.book_instance.book.title,
        'days_overdue': loan.days_overdue(),
    }
    
    notification = create_notification(
        user=loan.member.user,
        notification_type='OVERDUE',
        title=f'Overdue: {loan.book_instance.book.title}',
        message=f'Your book is {loan.days_overdue()} days overdue',
        priority=3
    )
    
    if loan.member.notification_preference and loan.member.notification_preference.email_enabled:
        send_notification_email(loan.member.user, 'OVERDUE', context)
        notification.sent_via_email = True
        notification.save()

def send_reservation_notification(reservation):
    context = {
        'user_name': reservation.member.user.get_full_name(),
        'book_title': reservation.book.title,
    }
    
    notification = create_notification(
        user=reservation.member.user,
        notification_type='RESERVED_AVAILABLE',
        title=f'Reserved book available: {reservation.book.title}',
        message='Your reserved book is now available for pickup',
        priority=2
    )
    
    if reservation.member.notification_preference and reservation.member.notification_preference.email_enabled:
        send_notification_email(reservation.member.user, 'RESERVED_AVAILABLE', context)
        notification.sent_via_email = True
        notification.save()
