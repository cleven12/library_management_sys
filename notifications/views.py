from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Notification, NotificationPreference
from accounts.models import MemberProfile

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]
    
    unread_count = notifications.filter(status__in=['PENDING', 'SENT']).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)

@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.status = 'READ'
    notification.read_at = timezone.now()
    notification.save()
    return redirect('notification_list')

@login_required
def notification_preferences(request):
    preference, created = NotificationPreference.objects.get_or_create(
        user=request.user
    )
    
    if request.method == 'POST':
        preference.email_enabled = request.POST.get('email_enabled') == 'on'
        preference.sms_enabled = request.POST.get('sms_enabled') == 'on'
        preference.push_enabled = request.POST.get('push_enabled') == 'on'
        preference.due_date_reminder = request.POST.get('due_date_reminder') == 'on'
        preference.overdue_notice = request.POST.get('overdue_notice') == 'on'
        preference.reservation_alert = request.POST.get('reservation_alert') == 'on'
        preference.new_books_alert = request.POST.get('new_books_alert') == 'on'
        preference.newsletter = request.POST.get('newsletter') == 'on'
        preference.save()
        
        return redirect('notification_preferences')
    
    return render(request, 'notifications/preferences.html', {
        'preference': preference
    })
