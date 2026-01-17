from django.contrib import admin
from .models import MemberProfile, LibrarianProfile, ActivityLog

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ['member_id', 'user', 'membership_type', 'status', 'membership_start']
    list_filter = ['membership_type', 'status', 'membership_start']
    search_fields = ['member_id', 'user__username', 'user__email', 'phone_number']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LibrarianProfile)
class LibrarianProfileAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'designation', 'is_active']
    list_filter = ['department', 'is_active', 'hire_date']
    search_fields = ['employee_id', 'user__username', 'department']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['timestamp', 'action']
    search_fields = ['user__username', 'action', 'details']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']
