import calendar
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Content, Category
from .forms import ContentForm

@csrf_exempt  # Убираем CSRF-защиту (лучше использовать `@csrf_protect`, если у тебя есть CSRF-токен)
def create_category(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            category, created = Category.objects.get_or_create(name=data["name"])
            return JsonResponse({"success": True, "id": category.id, "name": category.name})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'planner_app/category_list.html', {'categories': categories})



def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'Категория "{name}" добавлена!')
        else:
            messages.error(request, 'Название категории не может быть пустым!')

    return render(request, 'planner_app/create_category.html')



def content_list(request):
    contents = Content.objects.all().order_by('-created_at')  # Все записи, сортируем по дате создания
    return render(request, 'planner_app/content_list.html', {'contents': contents})

def content_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    return render(request, 'planner_app/content_detail.html', {'content': content})


def content_create(request):
    if request.method == 'POST':
        form = ContentForm(request.POST)
        new_category_name = request.POST.get('new_category_name')  # Получаем введённую категорию

        if form.is_valid():
            content = form.save(commit=False)  # Сначала не сохраняем в БД

            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                content.category = category
            else:
                content.category = form.cleaned_data['category']  # Берём из формы

            content.save()  # Теперь сохраняем с категорией
            messages.success(request, "Контент успешно создан!")
            return redirect('content_list')  # Замени на свою страницу

    else:
        form = ContentForm()

    return render(request, 'planner_app/content_create.html', {'form': form})

def content_update(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('content_detail', content_id=content.id)
    else:
        form = ContentForm(instance=content)
    return render(request, 'planner_app/content_update.html', {'form': form, 'content': content})

def content_delete(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if request.method == 'POST':
        content.delete()
        return redirect('content_list')
    return render(request, 'planner_app/content_delete.html', {'content': content})

def calendar_view(request, year=None, month=None):
    today = date.today()
    year = year if year else today.year
    month = month if month else today.month

    cal = calendar.Calendar(firstweekday=0)

    month_days = cal.itermonthdates(year, month)

    month_content = {}


    contents_in_month = Content.objects.filter(
        publish_date__year=year,
        publish_date__month=month
    )

    for single_day in month_days:
        month_content[single_day] = []

    for c in contents_in_month:
        publish_day = c.publish_date.date()
        # Добавим контент в соответствующий день
        if publish_day in month_content:
            month_content[publish_day].append(c)

    month_weeks = cal.monthdatescalendar(year, month)

    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_weeks': month_weeks,
        'month_content': month_content,
        'today': today,
    }
    return render(request, 'planner_app/calendar_view.html', context)

def base_context(request):
    """Добавляет список категорий во все шаблоны"""
    categories = Category.objects.all()
    return {'categories': categories}

def home(request):
    return render(request, 'planner_app/home.html')

def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            category.name = new_name
            category.save()
            return redirect('category_list')
    return render(request, 'planner_app/category_update.html', {'category': category})


def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'planner_app/category_delete.html', {'category': category})
