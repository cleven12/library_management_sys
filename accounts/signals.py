from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import MemberProfile
from notifications.models import NotificationPreference
from analytics.models import MemberActivity

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        member_id = f"MEM{instance.id:06d}"
        MemberProfile.objects.get_or_create(
            user=instance,
            defaults={'member_id': member_id}
        )
        NotificationPreference.objects.get_or_create(user=instance)

@receiver(post_save, sender=MemberProfile)
def create_member_activity(sender, instance, created, **kwargs):
    if created:
        MemberActivity.objects.get_or_create(member=instance)
