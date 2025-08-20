from django import forms
from .models import Nursery, VisitSchedule, VisitImpression


class NurseryForm(forms.ModelForm):
    class Meta:
        model = Nursery
        fields = [
            'facility_number', 'name', 'nursery_type', 'address', 'phone_number',
            'opening_time', 'closing_time', 'saturday_available',
            'capacity', 'age_from_months', 'age_to_years',
            'has_contact_app', 'contact_app_name',
            'has_school_bus', 'has_parking', 'has_lunch', 'has_allergy_support',
            'notes'
        ]
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'facility_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nursery_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_from_months': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_to_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_app_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VisitScheduleForm(forms.ModelForm):
    class Meta:
        model = VisitSchedule
        fields = ['nursery', 'visit_date', 'visit_time', 'status', 'contact_person', 'notes']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'visit_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nursery': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VisitImpressionForm(forms.ModelForm):
    class Meta:
        model = VisitImpression
        fields = [
            'nursery', 'visit_schedule',
            'overall_rating', 'facility_rating', 'staff_rating', 
            'education_rating', 'access_rating',
            'good_points', 'concern_points', 
            'staff_impression', 'children_atmosphere',
            'estimated_monthly_fee', 'application_intention', 'priority_rank',
            'photo1', 'photo2', 'photo3'
        ]
        widgets = {
            'good_points': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'concern_points': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'staff_impression': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'children_atmosphere': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nursery': forms.Select(attrs={'class': 'form-select'}),
            'visit_schedule': forms.Select(attrs={'class': 'form-select'}),
            'overall_rating': forms.Select(attrs={'class': 'form-select'}),
            'facility_rating': forms.Select(attrs={'class': 'form-select'}),
            'staff_rating': forms.Select(attrs={'class': 'form-select'}),
            'education_rating': forms.Select(attrs={'class': 'form-select'}),
            'access_rating': forms.Select(attrs={'class': 'form-select'}),
            'estimated_monthly_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'priority_rank': forms.NumberInput(attrs={'class': 'form-control'}),
        }