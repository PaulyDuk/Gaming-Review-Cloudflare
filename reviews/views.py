from django.shortcuts import render
from django.shortcuts import render
from django.views import generic
from .models import Review, Publisher, Developer, Comment


class ReviewList(generic.ListView):
    queryset = Review.objects.filter(is_published=True)
    template_name = "reviews/index.html"
    paginate_by = 6