from django.urls import path
from . import views
from .views.calendar import CalendarView

urlpatterns = [
    path('', views.home, name='home'),

    # Контент
    path('content/', views.content_list, name='content_list'),
    path('content/create/', views.content_create, name='content_create'),
    path('content/<int:content_id>/', views.content_detail, name='content_detail'),
    path('content/<int:content_id>/update/', views.content_update, name='content_update'),
    path('content/<int:content_id>/delete/', views.content_delete, name='content_delete'),

    # Категории
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/update/', views.category_update, name='category_update'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    # Календарь
    path('calendar/', CalendarView.as_view(), name='calendar_view'),
]
