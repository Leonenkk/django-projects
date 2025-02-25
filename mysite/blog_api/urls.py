from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from blog_api.views import PostList, UserPostList
from blog_api.views import PostDetail

urlpatterns=[
    path('',PostList.as_view(),name='post_list'),
    path('<int:pk>/',PostDetail.as_view(),name='post_detail'),
    path('user/<int:id>',UserPostList.as_view(),name='user_post_list'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]