from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from circulation.models import Loan, Reservation, Fine, CheckoutPolicy
from catalog.models import Book, BookInstance, Publisher
from accounts.models import MemberProfile

class LoanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.member = MemberProfile.objects.create(
            user=self.user,
            member_id='MEM001'
        )
        self.publisher = Publisher.objects.create(name='Test', country='USA')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publisher=self.publisher,
            publication_date=date.today(),
            pages=200
        )
        self.instance = BookInstance.objects.create(
            book=self.book,
            unique_id='INST001',
            location='A1'
        )
        self.loan = Loan.objects.create(
            book_instance=self.instance,
            member=self.member,
            due_date=date.today() + timedelta(days=14)
        )
    
    def test_loan_creation(self):
        self.assertEqual(self.loan.status, 'ACTIVE')
        self.assertEqual(self.loan.renewal_count, 0)
    
    def test_loan_not_overdue(self):
        self.assertFalse(self.loan.is_overdue())
    
    def test_loan_overdue(self):
        self.loan.due_date = date.today() - timedelta(days=1)
        self.loan.save()
        self.assertTrue(self.loan.is_overdue())
    
    def test_days_overdue_calculation(self):
        self.loan.due_date = date.today() - timedelta(days=5)
        self.loan.save()
        self.assertEqual(self.loan.days_overdue(), 5)

class CheckoutPolicyTests(TestCase):
    def test_policy_creation(self):
        policy = CheckoutPolicy.objects.create(
            membership_type='PREMIUM',
            max_books=10,
            loan_period_days=21,
            fine_per_day=0.25
        )
        self.assertEqual(policy.max_books, 10)
        self.assertEqual(policy.loan_period_days, 21)

class FineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.member = MemberProfile.objects.create(
            user=self.user,
            member_id='MEM001'
        )
    
    def test_fine_creation(self):
        fine = Fine.objects.create(
            member=self.member,
            amount=5.50,
            reason='OVERDUE',
            description='3 days overdue'
        )
        self.assertEqual(fine.status, 'PENDING')
        self.assertEqual(float(fine.amount), 5.50)
