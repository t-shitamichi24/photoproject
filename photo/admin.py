from django.contrib import admin

from .models import Category, PhotoPost

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'title')
  list_display_links = ('id', 'title')
admin.site.register(Category, CategoryAdmin)

class PhotoPostAdmin(admin.ModelAdmin):
  list_display = ('id', 'title')
  list_display_links = ('id', 'title')
admin.site.register(PhotoPost, PhotoPostAdmin)