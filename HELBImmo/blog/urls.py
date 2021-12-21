from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostStatsView,
    UserPostListView,
    FavoritesListView,
    SearchResultsListView
    )
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('search/', SearchResultsListView.as_view(), name='search-results'),
    path('favorites/', FavoritesListView.as_view(), name='user-favorites'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/stats/', PostStatsView.as_view(), name='post-stats'),
    path('about/', views.about, name='blog-about'),
    path('ajax/fav/', views.add_favorite, name='favorite'),
    path('ajax/consult/', views.post_consulted, name='post-consult'),
    path('ajax/question/new', views.post_question, name='question-new'),
    path('ajax/question/delete/<int:pk>', views.delete_question, name='question-delete'),
    path('ajax/question/answer', views.post_answer, name='answer-question'),
    path('ajax/question/answer/delete/<int:pk>', views.delete_answer, name='answer-delete')
]
