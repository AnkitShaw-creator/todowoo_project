from django.contrib import admin
from .models import ToDo
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields: list('datecreated',) #need to workon, field still not showing up

admin.site.register(ToDo, TodoAdmin)
