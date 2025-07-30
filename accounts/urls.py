
from django.urls import path
from reviews import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
]
