from django.contrib import admin
from .models import blogify

@admin.register(blogify)
class BlogifyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'author', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
