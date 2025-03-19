from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateField()

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('planned', 'Запланировано'),
        ('published', 'Опубликовано'),
    ]

    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)  # новое поле
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
