from django.shortcuts import render
from reviews.models import Review
from datetime import timedelta
from django.utils import timezone


def home_view(request):
    # Get the days filter parameter, default to 1 day
    days_filter = int(request.GET.get('days', 1))

    # Calculate the date threshold based on the filter
    filter_date = timezone.now() - timedelta(days=days_filter)

    # Filter reviews based on the selected time period
    review_list = Review.objects.filter(
        is_published=True, review_date__gte=filter_date
    ).order_by('-review_date')

    featured_reviews = Review.objects.filter(
        is_featured=True, is_published=True
    )

    is_paginated = False
    page_obj = None

    context = {
        'review_list': review_list,
        'featured_reviews': featured_reviews,
        'is_paginated': is_paginated,
        'page_obj': page_obj,
        'days_filter': days_filter,
    }
    return render(request, 'home/index.html', context)
