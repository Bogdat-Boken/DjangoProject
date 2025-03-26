from django import forms
from .models import Content, Category
from django.utils import timezone
from datetime import datetime

class ContentForm(forms.ModelForm):
    new_category = forms.CharField(required=False, max_length=255, label="Новая категория")
    published_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label="Дата публикации",
        required=True,
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Content
        fields = ['title', 'description', 'category', 'published_at']

    def clean_published_at(self):
        published_at = self.cleaned_data.get('published_at')
        if published_at:
            # Преобразуем naive datetime в aware datetime
            if timezone.is_naive(published_at):
                published_at = timezone.make_aware(published_at)
            
            # Сравниваем с текущим временем с учетом часового пояса
            now = timezone.now()
            if published_at < now:
                published_at = now
        return published_at

    def clean(self):
        cleaned_data = super().clean()
        new_category_name = cleaned_data.get("new_category")
        category = cleaned_data.get("category")

        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            cleaned_data["category"] = category
        elif not category:
            raise forms.ValidationError("Выберите категорию или введите новую.")

        return cleaned_data
