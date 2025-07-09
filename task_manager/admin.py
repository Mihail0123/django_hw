from django.contrib import admin
from .models import Task, SubTask, Category
from django.utils.html import format_html
from django.utils.timezone import now
from django.contrib.admin import SimpleListFilter

class OverdueFilter(SimpleListFilter):
    title = 'Overdue'
    parameter_name = 'is_overdue'

    def lookups(self, request, model_admin):
        return (
        ('yes', 'overdue'),
        ('no', 'not overdue'),
        )

    def queryset(self, request, queryset):
        today = now().date()
        if self.value() == 'yes':
            return queryset.filter(status__in=['NEW', 'IN_PROGRESS'], deadline__lt=today)
        elif self.value() == 'no':
            return queryset.exclude(status__in=['NEW', 'IN_PROGRESS'], deadline__lt=today)
        return queryset

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at') # колонки в списке задач
    list_filter = ('status', 'deadline', 'created_at') # фильтры справа
    search_fields = ('title', 'description') # поиск
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return (obj.title[:10] + '...') if len(obj.title) > 10 else obj.title

    short_title.short_description = 'Short title'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'colored_status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'created_at', 'task', OverdueFilter)
    search_fields = ('title', 'description')


    @admin.action(description='Set status to DONE')
    def mark_as_done(self, request, queryset):
        updated = queryset.update(status='DONE')
        self.message_user(request, f"{updated} subtask(s) marked as done.")

    actions = [mark_as_done]

    def colored_status(self, obj):
        color_map = {
            "NEW": 'red',
            "IN_PROGRESS": "orange",
            "DONE": "green",
        }
        color = color_map.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())

    colored_status.short_description = 'Status'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
