from django.urls import path

app_name='blog'
from apps.blog.views import PostListView, PostDetailView, PostFromCategoryView, CreatePostView, PostUpdateView, \
    CommentCreateView, PostByTagListView

urlpatterns=[
    path('', PostListView.as_view(), name='post_list'),
    path('post/create/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('post/<slug:slug>/update/',PostUpdateView.as_view(), name='update_post'),
    path('post/<slug:slug>/',PostDetailView.as_view(),name='post_detail'),
    path('post/tags/<slug:tag>/', PostByTagListView.as_view(), name='post_by_tag'),
    path('category/<slug:slug>/',PostFromCategoryView.as_view(),name='post_by_category'),

]