from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Avg
from analytics.models import BookPopularity, LibraryStatistics, MemberActivity
from catalog.models import Book
from circulation.models import Loan, Fine
from accounts.models import MemberProfile

class Command(BaseCommand):
    help = 'Update analytics and statistics'

    def handle(self, *args, **options):
        today = timezone.now().date()
        
        for book in Book.objects.all():
            total_loans = Loan.objects.filter(book_instance__book=book).count()
            total_reviews = book.reviews.count()
            avg_rating = book.average_rating
            
            popularity_score = (total_loans * 2) + (total_reviews * 1.5) + (float(avg_rating) * 10)
            
            BookPopularity.objects.update_or_create(
                book=book,
                defaults={
                    'total_loans': total_loans,
                    'total_reviews': total_reviews,
                    'average_rating': avg_rating,
                    'popularity_score': popularity_score,
                }
            )
        
        trending_books = BookPopularity.objects.order_by('-popularity_score')[:100]
        for rank, book_pop in enumerate(trending_books, 1):
            book_pop.trending_rank = rank
            book_pop.save()
        
        for profile in MemberProfile.objects.all():
            total_borrowed = Loan.objects.filter(member=profile).count()
            total_returned = Loan.objects.filter(member=profile, status='RETURNED').count()
            total_overdue = Loan.objects.filter(member=profile, status='OVERDUE').count()
            total_fines = Fine.objects.filter(member=profile, status='PAID').aggregate(
                total=Count('amount')
            )['total'] or 0
            total_reviews = profile.user.review_set.count()
            
            MemberActivity.objects.update_or_create(
                member=profile,
                defaults={
                    'total_books_borrowed': total_borrowed,
                    'total_books_returned': total_returned,
                    'total_overdue': total_overdue,
                    'total_reviews_written': total_reviews,
                    'last_activity': timezone.now(),
                }
            )
        
        total_members = MemberProfile.objects.count()
        active_members = MemberProfile.objects.filter(status='ACTIVE').count()
        total_books = Book.objects.count()
        books_on_loan = Loan.objects.filter(status='ACTIVE').count()
        overdue_books = Loan.objects.filter(status='OVERDUE').count()
        fines_collected = Fine.objects.filter(
            status='PAID',
            paid_date__date=today
        ).aggregate(total=Count('amount'))['total'] or 0
        
        LibraryStatistics.objects.update_or_create(
            date=today,
            defaults={
                'total_members': total_members,
                'active_members': active_members,
                'total_books': total_books,
                'books_on_loan': books_on_loan,
                'overdue_books': overdue_books,
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS('Analytics updated successfully')
        )
