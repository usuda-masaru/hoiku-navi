from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Avg
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from .models import Nursery, VisitSchedule, VisitImpression
from .forms import NurseryForm, VisitScheduleForm, VisitImpressionForm
from .utils import create_google_calendar_url, create_ics_content
import googlemaps
from django.conf import settings


@login_required
def home(request):
    context = {
        'total_nurseries': Nursery.objects.count(),
        'scheduled_visits': VisitSchedule.objects.filter(status='予定').count(),
        'completed_visits': VisitSchedule.objects.filter(status='完了').count(),
        'total_impressions': VisitImpression.objects.count(),
        'recent_schedules': VisitSchedule.objects.filter(
            status='予定',
            visit_date__gte=timezone.now().date()
        ).order_by('visit_date', 'visit_time')[:5],
        'top_rated': VisitImpression.objects.select_related('nursery').order_by('-overall_rating', '-created_at')[:5],
    }
    return render(request, 'nursery/home.html', context)


class NurseryListView(LoginRequiredMixin, ListView):
    model = Nursery
    template_name = 'nursery/nursery_list.html'
    context_object_name = 'nurseries'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        nursery_type = self.request.GET.get('type')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(facility_number__icontains=query)
            )
        
        if nursery_type:
            queryset = queryset.filter(nursery_type=nursery_type)
        
        return queryset.annotate(
            visit_count=Count('visit_schedules'),
            avg_rating=Avg('impressions__overall_rating')
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nursery_types'] = Nursery.NURSERY_TYPE_CHOICES
        return context


class NurseryDetailView(LoginRequiredMixin, DetailView):
    model = Nursery
    template_name = 'nursery/nursery_detail.html'
    context_object_name = 'nursery'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nursery = self.object
        context['schedules'] = nursery.visit_schedules.all().order_by('-visit_date')
        context['impressions'] = nursery.impressions.all().order_by('-created_at')
        context['avg_rating'] = nursery.impressions.aggregate(Avg('overall_rating'))['overall_rating__avg']
        return context


class NurseryCreateView(LoginRequiredMixin, CreateView):
    model = Nursery
    form_class = NurseryForm
    template_name = 'nursery/nursery_form.html'
    success_url = reverse_lazy('nursery:nursery_list')
    
    def form_valid(self, form):
        nursery = form.save(commit=False)
        
        # Google Maps APIを使用して緯度経度を取得
        if settings.GOOGLE_MAPS_API_KEY and nursery.address:
            try:
                gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
                geocode_result = gmaps.geocode(nursery.address)
                if geocode_result:
                    location = geocode_result[0]['geometry']['location']
                    nursery.latitude = location['lat']
                    nursery.longitude = location['lng']
            except Exception as e:
                messages.warning(self.request, f'住所から位置情報を取得できませんでした: {e}')
        
        nursery.save()
        messages.success(self.request, '保育園を登録しました。')
        return super().form_valid(form)


class NurseryUpdateView(LoginRequiredMixin, UpdateView):
    model = Nursery
    form_class = NurseryForm
    template_name = 'nursery/nursery_form.html'
    success_url = reverse_lazy('nursery:nursery_list')
    
    def form_valid(self, form):
        messages.success(self.request, '保育園情報を更新しました。')
        return super().form_valid(form)


class VisitScheduleListView(LoginRequiredMixin, ListView):
    model = VisitSchedule
    template_name = 'nursery/schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.select_related('nursery').order_by('visit_date', 'visit_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = VisitSchedule.STATUS_CHOICES
        return context


class VisitScheduleCreateView(LoginRequiredMixin, CreateView):
    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = 'nursery/schedule_form.html'
    success_url = reverse_lazy('nursery:schedule_list')
    
    def form_valid(self, form):
        messages.success(self.request, '見学スケジュールを登録しました。')
        return super().form_valid(form)


class VisitScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitSchedule
    form_class = VisitScheduleForm
    template_name = 'nursery/schedule_form.html'
    success_url = reverse_lazy('nursery:schedule_list')
    
    def form_valid(self, form):
        messages.success(self.request, '見学スケジュールを更新しました。')
        return super().form_valid(form)


class VisitImpressionListView(LoginRequiredMixin, ListView):
    model = VisitImpression
    template_name = 'nursery/impression_list.html'
    context_object_name = 'impressions'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        rating = self.request.GET.get('rating')
        application = self.request.GET.get('application')
        
        if rating:
            queryset = queryset.filter(overall_rating=rating)
        
        if application == 'true':
            queryset = queryset.filter(application_intention=True)
        
        return queryset.select_related('nursery', 'visit_schedule').order_by('-created_at')


class VisitImpressionCreateView(LoginRequiredMixin, CreateView):
    model = VisitImpression
    form_class = VisitImpressionForm
    template_name = 'nursery/impression_form.html'
    success_url = reverse_lazy('nursery:impression_list')
    
    def form_valid(self, form):
        messages.success(self.request, '見学感想を登録しました。')
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        nursery_id = self.request.GET.get('nursery')
        schedule_id = self.request.GET.get('schedule')
        
        if nursery_id:
            initial['nursery'] = nursery_id
        if schedule_id:
            initial['visit_schedule'] = schedule_id
        
        return initial


class VisitImpressionUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitImpression
    form_class = VisitImpressionForm
    template_name = 'nursery/impression_form.html'
    success_url = reverse_lazy('nursery:impression_list')
    
    def form_valid(self, form):
        messages.success(self.request, '見学感想を更新しました。')
        return super().form_valid(form)


@login_required
def map_view(request):
    nurseries = Nursery.objects.all().order_by('name')
    context = {
        'nurseries': nurseries,
    }
    return render(request, 'nursery/map_view.html', context)


@login_required
def schedule_to_calendar(request, pk):
    """見学スケジュールをGoogleカレンダーに追加"""
    schedule = get_object_or_404(VisitSchedule, pk=pk)
    calendar_url = create_google_calendar_url(schedule)
    return redirect(calendar_url)


@login_required
def schedule_download_ics(request, pk):
    """見学スケジュールをICSファイルでダウンロード"""
    schedule = get_object_or_404(VisitSchedule, pk=pk)
    ics_content = create_ics_content(schedule)
    
    response = HttpResponse(ics_content, content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename="nursery_visit_{pk}.ics"'
    return response
