from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Nursery(models.Model):
    NURSERY_TYPE_CHOICES = [
        ('認可保育園', '認可保育園'),
        ('認証保育園', '認証保育園'),
        ('無認可保育園', '無認可保育園'),
        ('幼稚園', '幼稚園'),
        ('認定こども園', '認定こども園'),
        ('小規模保育', '小規模保育'),
        ('企業主導型保育', '企業主導型保育'),
    ]
    
    facility_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='施設番号'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='保育園名'
    )
    nursery_type = models.CharField(
        max_length=20,
        choices=NURSERY_TYPE_CHOICES,
        verbose_name='施設タイプ'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='住所'
    )
    phone_regex = RegexValidator(
        regex=r'^[0-9-]+$',
        message='電話番号は数字とハイフンのみで入力してください'
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        verbose_name='電話番号'
    )
    
    # 保育時間
    opening_time = models.TimeField(
        verbose_name='開園時間',
        null=True,
        blank=True
    )
    closing_time = models.TimeField(
        verbose_name='閉園時間',
        null=True,
        blank=True
    )
    saturday_available = models.BooleanField(
        default=False,
        verbose_name='土曜保育'
    )
    
    # 施設情報
    capacity = models.IntegerField(
        verbose_name='定員',
        null=True,
        blank=True
    )
    age_from_months = models.IntegerField(
        verbose_name='受入開始月齢',
        null=True,
        blank=True,
        help_text='何ヶ月から'
    )
    age_to_years = models.IntegerField(
        verbose_name='受入終了年齢',
        null=True,
        blank=True,
        help_text='何歳まで'
    )
    
    # 連絡帳アプリ
    has_contact_app = models.BooleanField(
        default=False,
        verbose_name='連絡帳アプリ有無'
    )
    contact_app_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='連絡帳アプリ名'
    )
    
    # その他の設備・サービス
    has_school_bus = models.BooleanField(
        default=False,
        verbose_name='送迎バス'
    )
    has_parking = models.BooleanField(
        default=False,
        verbose_name='駐車場'
    )
    has_lunch = models.BooleanField(
        default=True,
        verbose_name='給食'
    )
    has_allergy_support = models.BooleanField(
        default=False,
        verbose_name='アレルギー対応'
    )
    
    # 位置情報（Google Maps用）
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='緯度'
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='経度'
    )
    
    # 自宅からの距離（自動計算用）
    distance_from_home = models.FloatField(
        null=True,
        blank=True,
        verbose_name='自宅からの距離(km)'
    )
    travel_time = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='自宅からの所要時間(分)'
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name='備考'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '保育園'
        verbose_name_plural = '保育園'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.name} ({self.nursery_type})'


class VisitSchedule(models.Model):
    STATUS_CHOICES = [
        ('予定', '予定'),
        ('完了', '完了'),
        ('キャンセル', 'キャンセル'),
    ]
    
    nursery = models.ForeignKey(
        Nursery,
        on_delete=models.CASCADE,
        related_name='visit_schedules',
        verbose_name='保育園'
    )
    visit_date = models.DateField(
        verbose_name='見学日'
    )
    visit_time = models.TimeField(
        verbose_name='見学時間',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='予定',
        verbose_name='ステータス'
    )
    contact_person = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='担当者名'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='メモ'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '見学スケジュール'
        verbose_name_plural = '見学スケジュール'
        ordering = ['visit_date', 'visit_time']
    
    def __str__(self):
        return f'{self.nursery.name} - {self.visit_date}'


class VisitImpression(models.Model):
    RATING_CHOICES = [
        (5, '★★★★★'),
        (4, '★★★★'),
        (3, '★★★'),
        (2, '★★'),
        (1, '★'),
    ]
    
    nursery = models.ForeignKey(
        Nursery,
        on_delete=models.CASCADE,
        related_name='impressions',
        verbose_name='保育園'
    )
    visit_schedule = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name='impression',
        verbose_name='見学スケジュール',
        null=True,
        blank=True
    )
    
    # 評価項目
    overall_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='総合評価'
    )
    facility_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='施設・設備',
        null=True,
        blank=True
    )
    staff_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='スタッフ・先生',
        null=True,
        blank=True
    )
    education_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='教育方針',
        null=True,
        blank=True
    )
    access_rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='アクセス',
        null=True,
        blank=True
    )
    
    # 詳細な感想
    good_points = models.TextField(
        verbose_name='良かった点'
    )
    concern_points = models.TextField(
        blank=True,
        verbose_name='気になった点'
    )
    staff_impression = models.TextField(
        blank=True,
        verbose_name='スタッフの印象'
    )
    children_atmosphere = models.TextField(
        blank=True,
        verbose_name='子どもたちの様子'
    )
    
    # 追加情報
    estimated_monthly_fee = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='想定月額費用(円)'
    )
    application_intention = models.BooleanField(
        default=False,
        verbose_name='申込意向'
    )
    priority_rank = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='優先順位'
    )
    
    # 写真
    photo1 = models.ImageField(
        upload_to='visit_photos/',
        blank=True,
        verbose_name='写真1'
    )
    photo2 = models.ImageField(
        upload_to='visit_photos/',
        blank=True,
        verbose_name='写真2'
    )
    photo3 = models.ImageField(
        upload_to='visit_photos/',
        blank=True,
        verbose_name='写真3'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '見学感想'
        verbose_name_plural = '見学感想'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.nursery.name} - 評価: {self.overall_rating}'
