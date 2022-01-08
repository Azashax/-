from django.contrib import admin

from request.models import RequestModel


@admin.register(RequestModel)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'organization', 'phone', 'approved']
    list_filter = ['approved']
    search_fields = ['organization']
    date_hierarchy = 'created_at'
    ordering = ['created_at']
