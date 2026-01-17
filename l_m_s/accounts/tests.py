from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import MemberProfile, LibrarianProfile, ActivityLog

class MemberProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = MemberProfile.objects.create(
            user=self.user,
            member_id='MEM000001',
            membership_type='STANDARD'
        )
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.member_id, 'MEM000001')
        self.assertEqual(self.profile.membership_type, 'STANDARD')
        self.assertEqual(self.profile.status, 'ACTIVE')
    
    def test_profile_string_representation(self):
        expected = f"{self.user.get_full_name()} - {self.profile.member_id}"
        self.assertEqual(str(self.profile), expected)
    
    def test_default_max_books(self):
        self.assertEqual(self.profile.max_books_allowed, 5)

class ActivityLogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        
    def test_activity_log_creation(self):
        log = ActivityLog.objects.create(
            user=self.user,
            action='LOGIN',
            details='User logged in',
            ip_address='127.0.0.1'
        )
        self.assertEqual(log.action, 'LOGIN')
        self.assertIsNotNone(log.timestamp)
