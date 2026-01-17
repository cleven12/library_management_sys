from django.core.management.base import BaseCommand
from django.utils import timezone
from circulation.models import Loan, CheckoutPolicy, Fine

class Command(BaseCommand):
    help = 'Mark overdue loans and generate fines'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        overdue_loans = Loan.objects.filter(
            status='ACTIVE',
            due_date__lt=today
        ).select_related('member', 'book_instance__book')
        
        count = 0
        for loan in overdue_loans:
            loan.status = 'OVERDUE'
            loan.save()
            
            days_overdue = (today - loan.due_date).days
            
            existing_fine = Fine.objects.filter(
                loan=loan,
                reason='OVERDUE',
                status='PENDING'
            ).first()
            
            if not existing_fine:
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
                    count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Processed {overdue_loans.count()} overdue loans, created {count} fines')
        )
