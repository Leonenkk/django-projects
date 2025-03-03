from django.urls import path

app_name='blog'
from apps.blog.views import PostListView, PostDetailView, PostFromCategoryView, CreatePostView

urlpatterns=[
    path('', PostListView.as_view(), name='post_list'),
    path('post/create/', CreatePostView.as_view(), name='create_post'),
    path('post/<slug:slug>/',PostDetailView.as_view(),name='post_detail'),
    path('category/<slug:slug>/',PostFromCategoryView.as_view(),name='post_by_category'),

]