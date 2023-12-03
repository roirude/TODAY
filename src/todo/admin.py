from django.contrib import admin


from todo.models import Task, History


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'complete', 'date_created']

admin.site.register(Task, TaskAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['task_completed', 'date_complete']

admin.site.register(History, HistoryAdmin)