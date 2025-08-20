from django.contrib import admin
from .models import Nursery, VisitSchedule, VisitImpression


@admin.register(Nursery)
class NurseryAdmin(admin.ModelAdmin):
    list_display = ['facility_number', 'name', 'nursery_type', 'address', 'phone_number']
    list_filter = ['nursery_type', 'saturday_available', 'has_contact_app', 'has_parking', 'has_lunch']
    search_fields = ['name', 'facility_number', 'address']
    fieldsets = (
        ('基本情報', {
            'fields': ('facility_number', 'name', 'nursery_type', 'address', 'phone_number')
        }),
        ('保育時間', {
            'fields': ('opening_time', 'closing_time', 'saturday_available')
        }),
        ('施設情報', {
            'fields': ('capacity', 'age_from_months', 'age_to_years')
        }),
        ('連絡帳アプリ', {
            'fields': ('has_contact_app', 'contact_app_name')
        }),
        ('設備・サービス', {
            'fields': ('has_school_bus', 'has_parking', 'has_lunch', 'has_allergy_support')
        }),
        ('位置情報', {
            'fields': ('latitude', 'longitude', 'distance_from_home', 'travel_time')
        }),
        ('その他', {
            'fields': ('notes',)
        }),
    )


@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ['nursery', 'visit_date', 'visit_time', 'status', 'contact_person']
    list_filter = ['status', 'visit_date']
    search_fields = ['nursery__name', 'contact_person']
    date_hierarchy = 'visit_date'
    ordering = ['-visit_date', 'visit_time']


@admin.register(VisitImpression)
class VisitImpressionAdmin(admin.ModelAdmin):
    list_display = ['nursery', 'overall_rating', 'application_intention', 'priority_rank', 'created_at']
    list_filter = ['overall_rating', 'application_intention']
    search_fields = ['nursery__name']
    fieldsets = (
        ('基本情報', {
            'fields': ('nursery', 'visit_schedule')
        }),
        ('評価', {
            'fields': ('overall_rating', 'facility_rating', 'staff_rating', 'education_rating', 'access_rating')
        }),
        ('感想', {
            'fields': ('good_points', 'concern_points', 'staff_impression', 'children_atmosphere')
        }),
        ('追加情報', {
            'fields': ('estimated_monthly_fee', 'application_intention', 'priority_rank')
        }),
        ('写真', {
            'fields': ('photo1', 'photo2', 'photo3')
        }),
    )
