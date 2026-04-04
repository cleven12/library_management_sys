from django.core.management.base import BaseCommand
from django.utils import timezone
from circulation.models import Loan
from notifications.models import Notification
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send due date reminders for books due in 3 days'

    def handle(self, *args, **options):
        today = timezone.now().date()
        reminder_date = today + timedelta(days=3)
        
        loans_due_soon = Loan.objects.filter(
            status='ACTIVE',
            due_date=reminder_date
        ).select_related('member__user', 'book_instance__book')
        
        count = 0
        for loan in loans_due_soon:
            if loan.member.notification_preference:
                Notification.objects.create(
                    user=loan.member.user,
                    notification_type='DUE_SOON',
                    title=f'Book due in 3 days: {loan.book_instance.book.title}',
                    message=f'Your borrowed book "{loan.book_instance.book.title}" is due on {loan.due_date}. Please return it on time to avoid fines.',
                    priority=2
                )
                count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Sent {count} due date reminders')
        )
