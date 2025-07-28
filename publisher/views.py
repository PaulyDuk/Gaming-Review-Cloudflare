from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Publisher
from reviews.models import Review

# Create your views here.


class PublisherList(generic.ListView):
    """List all publishers with pagination"""
    model = Publisher
    template_name = "publisher/publisher_list.html"
    context_object_name = 'publisher_list'
    paginate_by = 6
    ordering = ['name']


def publisher_games(request, publisher_id):
    """Show all games (reviews) by a specific publisher"""
    publisher = get_object_or_404(Publisher, id=publisher_id)
    games = Review.objects.filter(publisher=publisher, is_published=True)

    return render(request, 'publisher/publisher_games.html', {
        'publisher': publisher,
        'games': games
    })
