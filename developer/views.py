from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Developer
from reviews.models import Review

# Create your views here.


class DeveloperList(generic.ListView):
    """List all developers with pagination"""
    model = Developer
    template_name = "developer/developer_list.html"
    context_object_name = 'developer_list'
    paginate_by = 12
    ordering = ['name']


def developer_games(request, slug):
    """Show all games (reviews) by a specific developer"""
    developer = get_object_or_404(Developer, slug=slug)
    games = Review.objects.filter(developer=developer, is_published=True)

    return render(request, 'developer/developer_games.html', {
        'developer': developer,
        'games': games
    })
