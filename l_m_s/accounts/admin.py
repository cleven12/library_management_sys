from django.contrib import admin
from .models import MemberProfile

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'user', 'phone_number', 'status', 'membership_date')
    list_filter = ('status', 'membership_date')
    search_fields = ('member_id', 'user__username', 'user__email')
    ordering = ('-membership_date',)
