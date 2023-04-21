from django.contrib import admin

from task.models import Task

# Register your models here.
class TaskModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')

admin.site.register(Task, TaskModelAdmin)