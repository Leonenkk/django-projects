from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from blog.models import Post
from blog_api.serializers import PostSerializer
from blog_api.permissions import IsAuthorOrReadOnly


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']
    permission_classes = [IsAuthorOrReadOnly]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly]


class UserPostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        if user_id is None:
            return Post.objects.none()
        return Post.objects.filter(author=user_id)

