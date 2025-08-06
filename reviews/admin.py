from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Review, Publisher, Developer, UserComment, UserReview
# Register your models here.


class ReviewInline(admin.TabularInline):
    """Inline display of reviews for Publisher and Developer"""
    model = Review
    extra = 0  # Don't show extra empty forms
    fields = (
        'title', 'review_score', 'is_published',
        'is_featured', 'created_on'
    )
    readonly_fields = ('created_on',)
    show_change_link = True  # Allows clicking through to edit the full review
    list_editable = ('is_published', 'is_featured')  # Allow quick editing


@admin.register(Publisher)
class PublisherAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'founded_year', 'created_on')
    list_filter = ('founded_year', 'created_on')
    search_fields = ('name',)
    date_hierarchy = 'created_on'
    ordering = ('name',)
    list_per_page = 25
    inlines = [ReviewInline]  # Shows all games published by this publisher


@admin.register(Developer)
class DeveloperAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ('name', 'founded_year', 'created_on')
    list_filter = ('founded_year', 'created_on')
    search_fields = ('name',)
    date_hierarchy = 'created_on'
    ordering = ('name',)
    list_per_page = 25
    inlines = [ReviewInline]  # Shows all games developed by this developer


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'review_text')
    list_display = (
        'title', 'publisher', 'developer',
        'review_score', 'is_published', 'is_featured'
    )
    list_filter = (
        'is_published', 'is_featured', 'publisher', 'developer'
    )
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    list_per_page = 25
    actions = [
        'mark_as_published', 'mark_as_unpublished',
        'mark_as_featured', 'mark_as_unfeatured'
    ]

    def mark_as_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} reviews marked as published.')
    mark_as_published.short_description = "Mark selected reviews as published"

    def mark_as_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} reviews marked as unpublished.')
    mark_as_unpublished.short_description = "Mark selected as unpublished"

    def mark_as_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} reviews marked as featured.')
    mark_as_featured.short_description = "Mark selected reviews as featured"

    def mark_as_unfeatured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} reviews unmarked as featured.')
    mark_as_unfeatured.short_description = "Mark selected as not featured"


@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
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
    list_display = ('user', 'game', 'rating', 'created_on', 'approved')
    list_filter = ('rating', 'approved', 'created_on')
    search_fields = ('user__username', 'game__title', 'review_text')
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    list_per_page = 25
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)
    approve_reviews.short_description = "Mark selected reviews as approved"
