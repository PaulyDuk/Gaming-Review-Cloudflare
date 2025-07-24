from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Avg
from .models import Review, Publisher, Developer, Comment, UserReview
from .forms import CommentForm, UserReviewForm


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
    comments = review.comments.all().order_by("-created_on")
    comment_count = review.comments.filter(approved=True).count()

    # Get user reviews
    user_reviews = review.user_reviews.all().order_by("-created_on")
    user_review_count = user_reviews.count()

    # Calculate average review score
    average_review_score = None
    if user_review_count > 0:
        average_review_score = user_reviews.aggregate(Avg('rating'))['rating__avg']
        # Round to 1 decimal place
        average_review_score = round(average_review_score, 1)

    # Check if current user has already reviewed this game
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = UserReview.objects.filter(
            game=review, user=request.user
        ).exists()

    # Initialize forms for both GET and POST requests
    comment_form = CommentForm()
    user_review_form = UserReviewForm()

    if request.method == "POST":
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.review = review
                comment.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'Comment submitted and awaiting approval'
                )
                comment_form = CommentForm()

        elif 'review_submit' in request.POST and not user_has_reviewed:
            user_review_form = UserReviewForm(data=request.POST)
            if user_review_form.is_valid():
                user_review = user_review_form.save(commit=False)
                user_review.user = request.user
                user_review.game = review
                user_review.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    'Your review has been submitted successfully!'
                )
                user_review_form = UserReviewForm()
                user_has_reviewed = True

    return render(
        request,
        "reviews/review_detail.html",
        {
            "review": review,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "user_reviews": user_reviews,
            "user_review_count": user_review_count,
            "average_review_score": average_review_score,
            "user_review_form": user_review_form,
            "user_has_reviewed": user_has_reviewed,
        },
    )


def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Review.objects.filter(is_published=True)
        review = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('review_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Review.objects.filter(is_published=True)
    review = get_object_or_404(queryset, slug=slug)  # Changed from 'Review' to 'review'
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

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
