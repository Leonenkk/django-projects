from django.urls import path
from blog.views import post_list, post_detail, PostListView, share_post, post_comment

app_name='blog'

urlpatterns=[
    # path('',PostListView.as_view(),name='post_list'),
    path('',post_list,name='post_list'),
    path('<slug:tag_slug>/',post_list,name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail,name='post_detail'),
    path('<int:post_id>/share/',share_post,name='share_post'),
    path('<int:post_id>/comment/',post_comment,name='post_comment'),
]