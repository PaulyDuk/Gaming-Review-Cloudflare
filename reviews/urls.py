from . import views
from django.urls import path

app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewList.as_view(), name='review_list'),
    path('search/', views.search_games, name='search_games'),
    path('accounts/profile/', views.profile, name='profile'),
    path('<slug:slug>/', views.review_details, name='review_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>',
         views.user_comment_edit, name='user_comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.user_comment_delete, name='user_comment_delete'),
    path('<slug:slug>/edit_review/<int:review_id>',
         views.user_review_edit, name='user_review_edit'),
    path('<slug:slug>/delete_review/<int:review_id>',
         views.user_review_delete, name='user_review_delete'),
]
