from django.contrib import admin
from .models import Task, SubTask, Category

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
    list_display = ('title', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline', 'created_at', 'task')
    search_fields = ('title', 'description')

    @admin.action(description='Set status to DONE')
    def mark_as_done(self, request, queryset):
        updated = queryset.update(status='DONE')
        self.message_user(request, f"{updated} subtask(s) marked as done.")

    actions = [mark_as_done]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
