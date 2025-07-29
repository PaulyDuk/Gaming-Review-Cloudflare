from django.urls import path
from . import views

app_name = 'publisher'

urlpatterns = [
    path('', views.PublisherList.as_view(), name='publisher_list'),
    path('<slug:slug>/', views.publisher_games, name='publisher_games'),
]
