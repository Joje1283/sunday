from django.contrib import admin
from .models import Grant, Use


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'days']


@admin.register(Use)
class UseAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'days', 'start_date', 'end_date', 'approve', 'cancel']
