from . import views
from django.urls import path

urlpatterns = [
    path('', views.ReviewList.as_view(), name='home'),
    path('search/', views.search_games, name='search_games'),
    path('publisher/<int:publisher_id>/', views.publisher_games, name='publisher_games'),
    path('developer/<int:developer_id>/', views.developer_games, name='developer_games'),
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
