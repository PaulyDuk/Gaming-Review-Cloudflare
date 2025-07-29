from django.urls import path
from . import views

app_name = 'developer'

urlpatterns = [
    path('', views.DeveloperList.as_view(), name='developer_list'),
    path('<slug:slug>/', views.developer_games, name='developer_games'),
]
