from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.ReviewList.as_view(), name='home'),
    path("accounts/", include("allauth.urls")),
    path('<slug:slug>/', views.review_details, name='review_detail'),
    path('search/', views.search_games, name='search_games'),
]