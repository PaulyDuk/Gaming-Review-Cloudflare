from django.urls import path
from reviews import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
]
