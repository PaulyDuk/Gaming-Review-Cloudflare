from django.shortcuts import render
from django.core.paginator import Paginator
from reviews.models import Review
from datetime import timedelta
from django.utils import timezone


def home_view(request):
    # Get the days filter parameter, default to 7 days
    days_filter = int(request.GET.get('days', 7))

    # Calculate the date threshold based on the filter
    filter_date = timezone.now() - timedelta(days=days_filter)

    # Filter reviews based on the selected time period
    review_queryset = Review.objects.filter(
        is_published=True, review_date__gte=filter_date
    ).order_by('-review_date')

    # Pagination for recent reviews
    paginator = Paginator(review_queryset, 16)  # 16 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if pagination is needed
    is_paginated = paginator.num_pages > 1

    featured_reviews = Review.objects.filter(
        is_featured=True, is_published=True
    )

    context = {
        'review_list': page_obj,
        'featured_reviews': featured_reviews,
        'is_paginated': is_paginated,
        'page_obj': page_obj,
        'paginator': paginator,
        'days_filter': days_filter,
    }
    return render(request, 'home/index.html', context)
