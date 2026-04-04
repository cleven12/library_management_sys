from django.contrib import admin
from .models import BookPopularity, MemberActivity, LibraryStatistics, SearchLog

@admin.register(BookPopularity)
class BookPopularityAdmin(admin.ModelAdmin):
    list_display = ['book', 'total_loans', 'total_reservations', 'average_rating', 'popularity_score', 'trending_rank']
    list_filter = ['last_borrowed', 'trending_rank']
    search_fields = ['book__title']
    readonly_fields = ['updated_at']

@admin.register(MemberActivity)
class MemberActivityAdmin(admin.ModelAdmin):
    list_display = ['member', 'total_books_borrowed', 'total_books_returned', 'total_overdue', 'reading_streak_days']
    search_fields = ['member__user__username', 'member__member_id']
    readonly_fields = ['updated_at']

@admin.register(LibraryStatistics)
class LibraryStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_members', 'active_members', 'books_on_loan', 'overdue_books', 'fines_collected']
    list_filter = ['date']
    date_hierarchy = 'date'

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ['search_query', 'user', 'results_count', 'timestamp', 'ip_address']
    list_filter = ['timestamp']
    search_fields = ['search_query', 'user__username']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']
