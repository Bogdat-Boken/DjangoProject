from django import forms
from .models import Content, Category

class ContentForm(forms.ModelForm):
    new_category = forms.CharField(required=False, max_length=255, label="Новая категория")

    class Meta:
        model = Content
        fields = ['title', 'description', 'category', 'published_at']

    def clean(self):
        cleaned_data = super().clean()
        new_category_name = cleaned_data.get("new_category")
        category = cleaned_data.get("category")

        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            cleaned_data["category"] = category  # Присваиваем новосозданную категорию
        elif not category:
            raise forms.ValidationError("Выберите категорию или введите новую.")

        return cleaned_data
