from django.contrib import admin
from .models import Notification, NotificationPreference, EmailTemplate

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'status', 'priority', 'created_at']
    list_filter = ['notification_type', 'status', 'priority', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'sent_at', 'read_at']

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_enabled', 'sms_enabled', 'push_enabled']
    search_fields = ['user__username']

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'notification_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'notification_type']
    search_fields = ['name', 'subject']
    readonly_fields = ['created_at', 'updated_at']
