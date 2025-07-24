from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Review, Publisher, Developer, Comment, UserReview
# Register your models here.


class ReviewInline(admin.TabularInline):
    """Inline display of reviews for Publisher and Developer"""
    model = Review
    extra = 0  # Don't show extra empty forms
    fields = (
        'title', 'genre', 'console', 'review_score', 'is_published',
        'is_featured', 'created_on'
    )
    readonly_fields = ('created_on',)
    show_change_link = True  # Allows clicking through to edit the full review


@admin.register(Publisher)
class PublisherAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'founded_year', 'headquarters', 'created_on')
    list_filter = ('founded_year', 'created_on')
    search_fields = ('name', 'headquarters')
    date_hierarchy = 'created_on'
    ordering = ('name',)
    list_per_page = 25
    inlines = [ReviewInline]  # Shows all games published by this publisher


@admin.register(Developer)
class DeveloperAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'founded_year', 'headquarters', 'created_on')
    list_filter = ('founded_year', 'created_on')
    search_fields = ('name', 'headquarters')
    date_hierarchy = 'created_on'
    ordering = ('name',)
    list_per_page = 25
    inlines = [ReviewInline]  # Shows all games developed by this developer


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'review_text')
    list_display = (
        'title', 'publisher', 'developer', 'genre', 'console',
        'review_score', 'is_published'
    )
    list_filter = (
        'genre', 'console', 'is_published', 'publisher', 'developer'
    )
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    list_per_page = 25


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'review', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('author__username', 'body')
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    list_per_page = 25
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Mark selected comments as approved"

@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'created_on')
    list_filter = ('rating', 'created_on')
    search_fields = ('user__username', 'game__title')
