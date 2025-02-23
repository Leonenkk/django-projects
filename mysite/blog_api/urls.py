from django.urls import path

from blog_api.views import PostList, UserPostList
from blog_api.views import PostDetail

urlpatterns=[
    path('',PostList.as_view(),name='post_list'),
    path('<int:pk>/',PostDetail.as_view(),name='post_detail'),
    path('user/<int:id>',UserPostList.as_view(),name='user_post_list'),
]