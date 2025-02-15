from django.urls import path
from blog import views

app_name='blog'

urlpatterns=[
    path('',views.post_list,name='post_list'),
    path('search/', views.post_search, name='post_search'),
    path('<slug:tag_slug>/',views.post_list,name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.share_post,name='share_post'),
    path('<int:post_id>/comment/',views.post_comment,name='post_comment'),
]