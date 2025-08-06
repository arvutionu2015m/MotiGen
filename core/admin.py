from django.contrib import admin
from .models import CVEntry

@admin.register(CVEntry)
class CVEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'content')
    ordering = ('-created_at',)
