from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import UserComment, UserReview


@user_passes_test(lambda u: u.is_superuser)
def approve_comments(request):
    """View for approving user comments"""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ['approve', 'reject']:
            comment_ids = request.POST.getlist('comment_ids')
            if action == 'approve':
                UserComment.objects.filter(id__in=comment_ids).update(
                    approved=True)
                messages.success(
                    request, f'Approved {len(comment_ids)} comment(s)')
            elif action == 'reject':
                UserComment.objects.filter(id__in=comment_ids).delete()
                messages.success(
                    request, f'Deleted {len(comment_ids)} comment(s)')

        elif action == 'delete_approved':
            approved_comment_ids = request.POST.getlist('approved_comment_ids')
            if approved_comment_ids:
                UserComment.objects.filter(
                    id__in=approved_comment_ids).delete()
                messages.success(
                    request,
                    f'Deleted {len(approved_comment_ids)} approved comment(s)')

    # Get all unapproved comments
    unapproved_comments = UserComment.objects.filter(
        approved=False
    ).order_by('-created_on')

    # Get recently approved comments for reference
    recent_approved = UserComment.objects.filter(
        approved=True
    ).order_by('-created_on')[:10]

    context = {
        'unapproved_comments': unapproved_comments,
        'recent_approved': recent_approved,
        'total_unapproved': unapproved_comments.count(),
    }

    return render(request, 'reviews/approve_comments.html', context)


@user_passes_test(lambda u: u.is_superuser)
def approve_reviews(request):
    """View for approving user reviews"""
    if request.method == 'POST':
        action = request.POST.get('action')

        if action in ['approve', 'reject']:
            review_ids = request.POST.getlist('review_ids')
            if action == 'approve':
                UserReview.objects.filter(id__in=review_ids).update(
                    approved=True)
                messages.success(
                    request, f'Approved {len(review_ids)} review(s)')
            elif action == 'reject':
                UserReview.objects.filter(id__in=review_ids).delete()
                messages.success(
                    request, f'Deleted {len(review_ids)} review(s)')

        elif action == 'delete_approved':
            approved_review_ids = request.POST.getlist('approved_review_ids')
            if approved_review_ids:
                UserReview.objects.filter(id__in=approved_review_ids).delete()
                messages.success(
                    request,
                    f'Deleted {len(approved_review_ids)} approved review(s)')

    # Get all unapproved reviews
    unapproved_reviews = UserReview.objects.filter(
        approved=False
    ).order_by('-created_on')

    # Get recently approved reviews for reference
    recent_approved = UserReview.objects.filter(
        approved=True
    ).order_by('-created_on')[:10]

    context = {
        'unapproved_reviews': unapproved_reviews,
        'recent_approved': recent_approved,
        'total_unapproved': unapproved_reviews.count(),
    }

    return render(request, 'reviews/approve_reviews.html', context)
