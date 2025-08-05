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

    def get_queryset(self):
        queryset = Developer.objects.all()
        sort = self.request.GET.get('sort')
        if sort == 'az':
            queryset = queryset.order_by('name')
        elif sort == 'za':
            queryset = queryset.order_by('-name')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_on')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_on')
        else:
            queryset = queryset.order_by('name')  # Default ordering
        return queryset


def developer_games(request, slug):
    """Show all games (reviews) by a specific developer"""
    developer = get_object_or_404(Developer, slug=slug)
    games = Review.objects.filter(developer=developer, is_published=True)

    return render(request, 'developer/developer_games.html', {
        'developer': developer,
        'games': games
    })
