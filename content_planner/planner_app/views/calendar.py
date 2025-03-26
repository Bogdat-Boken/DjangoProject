from datetime import datetime, timedelta
from calendar import monthcalendar
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils import timezone
from ..models import Content

class CalendarView(TemplateView):
    template_name = 'planner_app/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current year and month
        today = timezone.now()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        
        # Get calendar data
        cal = monthcalendar(year, month)
        
        # Get content for this month
        start_date = timezone.make_aware(datetime(year, month, 1))
        if month == 12:
            end_date = timezone.make_aware(datetime(year + 1, 1, 1))
        else:
            end_date = timezone.make_aware(datetime(year, month + 1, 1))
            
        content_list = Content.objects.filter(
            scheduled_date__gte=start_date,
            scheduled_date__lt=end_date
        ).select_related('category', 'created_by')
        
        # Create calendar data structure
        calendar_data = []
        for week in cal:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append({
                        'day': None,
                        'content': []
                    })
                else:
                    day_content = [
                        content for content in content_list
                        if content.scheduled_date.day == day
                    ]
                    week_data.append({
                        'day': day,
                        'today': today.day == day and today.month == month and today.year == year,
                        'content': day_content
                    })
            calendar_data.append(week_data)
            
        # Previous and next month links
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
            
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
            
        context.update({
            'calendar': calendar_data,
            'current_month': datetime(year, month, 1),
            'prev_month': {'year': prev_year, 'month': prev_month},
            'next_month': {'year': next_year, 'month': next_month},
        })
        
        return context 