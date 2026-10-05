from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at")
    list_filter = ("status", "category", "created_at", "updated_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)