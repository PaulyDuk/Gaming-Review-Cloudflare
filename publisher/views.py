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
    paginate_by = 12

    def get_queryset(self):
        queryset = Publisher.objects.all()
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


def publisher_games(request, slug):
    """Show all games (reviews) by a specific publisher"""
    publisher = get_object_or_404(Publisher, slug=slug)
    games = Review.objects.filter(publisher=publisher, is_published=True)

    return render(request, 'publisher/publisher_games.html', {
        'publisher': publisher,
        'games': games
    })
