from django.urls import path
from . import views
from . import auth_views

app_name = 'nursery'

urlpatterns = [
    # 認証
    path('login/', auth_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', auth_views.signup, name='signup'),
    
    path('', auth_views.CustomLoginView.as_view(), name='home'),
    
    # 保育園
    path('nurseries/', views.NurseryListView.as_view(), name='nursery_list'),
    path('nursery/<int:pk>/', views.NurseryDetailView.as_view(), name='nursery_detail'),
    path('nursery/new/', views.NurseryCreateView.as_view(), name='nursery_create'),
    path('nursery/<int:pk>/edit/', views.NurseryUpdateView.as_view(), name='nursery_update'),
    
    # 見学スケジュール
    path('schedules/', views.VisitScheduleListView.as_view(), name='schedule_list'),
    path('schedule/new/', views.VisitScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/<int:pk>/edit/', views.VisitScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedule/<int:pk>/calendar/', views.schedule_to_calendar, name='schedule_to_calendar'),
    path('schedule/<int:pk>/ics/', views.schedule_download_ics, name='schedule_download_ics'),
    
    # 見学感想
    path('impressions/', views.VisitImpressionListView.as_view(), name='impression_list'),
    path('impression/new/', views.VisitImpressionCreateView.as_view(), name='impression_create'),
    path('impression/<int:pk>/edit/', views.VisitImpressionUpdateView.as_view(), name='impression_update'),
    
    # マップ
    path('map/', views.map_view, name='map_view'),
]