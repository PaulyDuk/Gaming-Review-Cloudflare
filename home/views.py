from django.shortcuts import render
from reviews.models import Review
from datetime import timedelta
from django.utils import timezone


def home_view(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    # Use the same logic as ReviewList view for consistency
    review_list = Review.objects.filter(
        is_published=True, review_date__gte=seven_days_ago)
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
    }
    return render(request, 'home/index.html', context)
