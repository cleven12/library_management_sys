from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import MemberProfile
from accounts.premium_models import Badge, MemberBadge
from circulation.models import Loan
from catalog.models import Review

class Command(BaseCommand):
    help = 'Award badges to members based on achievements'

    def handle(self, *args, **options):
        self.award_reading_badges()
        self.award_review_badges()
        self.award_milestone_badges()
        
        self.stdout.write(
            self.style.SUCCESS('Badge awarding complete')
        )
    
    def award_reading_badges(self):
        """Award badges for reading achievements"""
        bookworm, _ = Badge.objects.get_or_create(
            name='Bookworm',
            defaults={
                'description': 'Read 10 books',
                'category': 'READING',
                'requirement': {'books_read': 10},
                'points': 50
            }
        )
        
        for profile in MemberProfile.objects.all():
            books_read = Loan.objects.filter(
                member=profile,
                status='RETURNED'
            ).count()
            
            if books_read >= 10:
                MemberBadge.objects.get_or_create(
                    member=profile,
                    badge=bookworm
                )
    
    def award_review_badges(self):
        """Award badges for writing reviews"""
        critic, _ = Badge.objects.get_or_create(
            name='Book Critic',
            defaults={
                'description': 'Write 5 reviews',
                'category': 'PARTICIPATION',
                'requirement': {'reviews_written': 5},
                'points': 30
            }
        )
        
        for user in User.objects.all():
            reviews_count = Review.objects.filter(user=user).count()
            
            if reviews_count >= 5:
                try:
                    profile = user.profile
                    MemberBadge.objects.get_or_create(
                        member=profile,
                        badge=critic
                    )
                except MemberProfile.DoesNotExist:
                    pass
    
    def award_milestone_badges(self):
        """Award milestone badges"""
        pioneer, _ = Badge.objects.get_or_create(
            name='Library Pioneer',
            defaults={
                'description': 'First 100 members',
                'category': 'MILESTONE',
                'requirement': {'member_rank': 100},
                'points': 100
            }
        )
        
        early_members = MemberProfile.objects.order_by('created_at')[:100]
        
        for profile in early_members:
            MemberBadge.objects.get_or_create(
                member=profile,
                badge=pioneer
            )
