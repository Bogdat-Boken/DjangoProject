from django.urls import path
from . import views
from .views import (
    content_list, content_detail, content_create, content_update, content_delete,
    create_category, category_list, category_update, category_delete, calendar_view
)

urlpatterns = [
    path('', views.home, name='home'),
    path('content/', views.content_list, name='content_list'),
    path('content/create/', views.content_create, name='content_create'),
    path('categories/', views.category_list, name='category_list'),

    # Контент
    path('content/<int:content_id>/', content_detail, name='content_detail'),
    path('content/<int:content_id>/update/', content_update, name='content_update'),
    path('content/<int:content_id>/delete/', content_delete, name='content_delete'),

    # Категории
    path('categories/create/', create_category, name='create_category'),
    path('categories/<int:category_id>/update/', views.category_update, name='category_update'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    # Главная
    path('', views.home, name='home'),

    # Календарь
    path('calendar/', calendar_view, name='calendar_view'),
    path('calendar/<int:year>/<int:month>/', calendar_view, name='calendar_view_month'),
]
