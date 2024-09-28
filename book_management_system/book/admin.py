from django.contrib import admin
from .models import Book, Review

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'year_published', 'created_at', 'updated_at')
    search_fields = ('title', 'author__username', 'genre')
    list_filter = ('genre', 'year_published','genre')
    ordering = ('-year_published',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at', 'updated_at')
    search_fields = ('book__title', 'user__username', 'review_text')
    list_filter = ('rating',)
    ordering = ('-created_at',)

# Register the models with the admin site
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)