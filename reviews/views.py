from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Avg, Q
from .models import Review, Publisher, Developer, UserComment, UserReview
from .forms import UserCommentForm, UserReviewForm


# Create your views here.


class ReviewList(generic.ListView):
    queryset = Review.objects.filter(is_published=True)
    template_name = "reviews/index.html"
    paginate_by = 6


def review_details(request, slug):
    """
    Display an individual :model:`reviews.Review`.

    **Context**

    ``review``
        An instance of :model:`reviews.Review`.

    **Template:**

    :template:`reviews/review_detail.html`
    """

    queryset = Review.objects.filter(is_published=True)
    review = get_object_or_404(queryset, slug=slug)
    user_comments = review.user_comments.all().order_by("-created_on")
    comment_count = review.user_comments.filter(approved=True).count()

    # Get user reviews - show approved ones + current user's unapproved ones
    if request.user.is_authenticated:
        user_reviews = review.user_reviews.filter(
            Q(approved=True) | Q(user=request.user)
        ).order_by("-created_on")
    else:
        user_reviews = review.user_reviews.filter(
            approved=True
        ).order_by("-created_on")
    
    # Count only approved reviews for the public count
    user_review_count = review.user_reviews.filter(approved=True).count()

    # Calculate average review score - only from approved reviews
    average_review_score = None
    if user_review_count > 0:
        approved_reviews = review.user_reviews.filter(approved=True)
        average_review_score = approved_reviews.aggregate(
            Avg('rating')
        )['rating__avg']
        # Round to 1 decimal place
        average_review_score = round(average_review_score, 1)

    # Check if current user has already reviewed this game
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = UserReview.objects.filter(
            game=review, user=request.user
        ).exists()

    # Initialize forms for both GET and POST requests
    user_comment_form = UserCommentForm()
    user_review_form = UserReviewForm()

    if request.method == "POST":
        if 'comment_submit' in request.POST:
            user_comment_form = UserCommentForm(data=request.POST)
            if user_comment_form.is_valid():
                user_comment = user_comment_form.save(commit=False)
                user_comment.author = request.user
                user_comment.review = review
                user_comment.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'Comment submitted and awaiting approval'
                )
                user_comment_form = UserCommentForm()

        elif 'review_submit' in request.POST and not user_has_reviewed:
            user_review_form = UserReviewForm(data=request.POST)
            if user_review_form.is_valid():
                user_review = user_review_form.save(commit=False)
                user_review.user = request.user
                user_review.game = review
                user_review.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'Review submitted and awaiting approval'
                )
                user_review_form = UserReviewForm()
                user_has_reviewed = True

    return render(
        request,
        "reviews/review_detail.html",
        {
            "review": review,
            "user_comments": user_comments,
            "comment_count": comment_count,
            "user_comment_form": user_comment_form,
            "user_reviews": user_reviews,
            "user_review_count": user_review_count,
            "average_review_score": average_review_score,
            "user_review_form": user_review_form,
            "user_has_reviewed": user_has_reviewed,
        },
    )


def user_comment_edit(request, slug, comment_id):
    """
    view to edit user comments
    """
    if request.method == "POST":

        queryset = Review.objects.filter(is_published=True)
        review = get_object_or_404(queryset, slug=slug)
        user_comment = get_object_or_404(UserComment, pk=comment_id)
        user_comment_form = UserCommentForm(
            data=request.POST, instance=user_comment
        )

        if (user_comment_form.is_valid() and
                user_comment.author == request.user):
            user_comment = user_comment_form.save(commit=False)
            user_comment.review = review
            user_comment.approved = False
            user_comment.save()
            messages.add_message(
                request, messages.SUCCESS, 'Comment Updated!'
            )
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating comment!'
            )

    return HttpResponseRedirect(reverse('review_detail', args=[slug]))


def user_comment_delete(request, slug, comment_id):
    """
    view to delete user comment
    """
    queryset = Review.objects.filter(is_published=True)
    review = get_object_or_404(queryset, slug=slug)
    user_comment = get_object_or_404(UserComment, pk=comment_id)

    # Ensure the comment belongs to this review
    if user_comment.review != review:
        messages.add_message(request, messages.ERROR, 'Comment not found!')
        return HttpResponseRedirect(reverse('review_detail', args=[slug]))

    if user_comment.author == request.user:
        user_comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own comments!'
        )

    return HttpResponseRedirect(reverse('review_detail', args=[slug]))


def user_review_edit(request, slug, review_id):
    """
    view to edit user reviews
    """
    if request.method == "POST":

        queryset = Review.objects.filter(is_published=True)
        review = get_object_or_404(queryset, slug=slug)
        user_review = get_object_or_404(UserReview, pk=review_id)
        user_review_form = UserReviewForm(
            data=request.POST, instance=user_review
        )

        # Ensure the review belongs to this game
        if user_review.game != review:
            messages.add_message(request, messages.ERROR, 'Review not found!')
            return HttpResponseRedirect(reverse('review_detail', args=[slug]))

        if user_review_form.is_valid() and user_review.user == request.user:
            user_review = user_review_form.save(commit=False)
            user_review.game = review
            user_review.save()
            messages.add_message(request, messages.SUCCESS, 'Review Updated!')
        else:
            messages.add_message(
                request, messages.ERROR, 'Error updating review!'
            )

    return HttpResponseRedirect(reverse('review_detail', args=[slug]))


def user_review_delete(request, slug, review_id):
    """
    view to delete user review
    """
    queryset = Review.objects.filter(is_published=True)
    review = get_object_or_404(queryset, slug=slug)
    user_review = get_object_or_404(UserReview, pk=review_id)

    # Ensure the review belongs to this game
    if user_review.game != review:
        messages.add_message(request, messages.ERROR, 'Review not found!')
        return HttpResponseRedirect(reverse('review_detail', args=[slug]))

    if user_review.user == request.user:
        user_review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted!')
    else:
        messages.add_message(
            request, messages.ERROR, 'You can only delete your own reviews!'
        )

    return HttpResponseRedirect(reverse('review_detail', args=[slug]))


def publisher_games(request, publisher_id):
    """Show all games (reviews) by a specific publisher"""
    publisher = get_object_or_404(Publisher, id=publisher_id)
    games = Review.objects.filter(publisher=publisher, is_published=True)

    return render(request, 'reviews/publisher_games.html', {
        'publisher': publisher,
        'games': games
    })


def developer_games(request, developer_id):
    """Show all games (reviews) by a specific developer"""
    developer = get_object_or_404(Developer, id=developer_id)
    games = Review.objects.filter(developer=developer, is_published=True)

    return render(request, 'reviews/developer_games.html', {
        'developer': developer,
        'games': games
    })


def search_games(request):
    """Search for games, publishers, developers and genres"""
    query = request.GET.get('q', '')

    if query:
        # Search games by title
        games_by_title = Review.objects.filter(
            title__icontains=query,
            is_published=True
        )

        # Search games by genre
        games_by_genre = Review.objects.filter(
            genre__icontains=query,
            is_published=True
        )

        # Combine and remove duplicates
        games = (games_by_title | games_by_genre).distinct()

        # Search publishers
        publishers = Publisher.objects.filter(name__icontains=query)

        # Search developers
        developers = Developer.objects.filter(name__icontains=query)

        return render(request, 'reviews/search_results.html', {
            'query': query,
            'games': games,
            'publishers': publishers,
            'developers': developers
        })

    return render(request, 'reviews/search_results.html', {'query': query})
