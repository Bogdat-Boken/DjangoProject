from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#4a90e2")  # HEX color
    
    def __str__(self):
        return self.name

class MediaLibrary(models.Model):
    file = models.FileField(upload_to='media_library/')
    title = models.CharField(max_length=200)
    file_type = models.CharField(max_length=50)  # image, video, etc.
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Media Library"

class ContentTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    structure = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Content(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На рассмотрении'),
        ('scheduled', 'Запланирован'),
        ('published', 'Опубликован'),
        ('archived', 'В архиве'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    template = models.ForeignKey(ContentTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    media_files = models.ManyToManyField(MediaLibrary, blank=True)
    
    # Scheduling
    scheduled_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    # Team and tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_content')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_content')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Analytics
    views_count = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.title
    
    def publish(self):
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()

class ContentHistory(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(default=timezone.now)
    changes = models.JSONField()  # Store what was changed
    
    def __str__(self):
        return f"Change to {self.content.title} by {self.changed_by.username}"

class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.content.title}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('deadline', 'Дедлайн'),
        ('mention', 'Упоминание'),
        ('comment', 'Комментарий'),
        ('status_change', 'Изменение статуса'),
        ('assignment', 'Назначение'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class Checklist(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    items = models.JSONField()  # List of checklist items with completion status
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Checklist for {self.content.title}"

class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    account_name = models.CharField(max_length=100)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, blank=True)
    connected_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.platform} - {self.account_name}"

class Analytics(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    date = models.DateField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    platform = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "Analytics"
        
    def __str__(self):
        return f"Analytics for {self.content.title} on {self.date}"
