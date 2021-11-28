from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostStatsView,
    UserPostListView,
    FavoritesListView
    )
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('favorites/', FavoritesListView.as_view(), name='user-favorites'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/stats/', PostStatsView.as_view(), name='post-stats'),
    path('about/', views.about, name='blog-about'),
    path('ajax/fav/', views.add_favorite, name='favorite'),
    path('ajax/consult', views.post_consulted, name='post-consult')
]
