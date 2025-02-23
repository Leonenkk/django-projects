from rest_framework import serializers
from blog import models

class CommentSerializer(serializers.Serializer):
    email=serializers.EmailField()
    content=serializers.CharField(max_length=200)
    created=serializers.DateTimeField()

    def create(self,validated_data):
        comment=models.Comment.objects.create(**validated_data)
        return comment

    def update(self,instance,validated_data):
        instance.email=validated_data.get('content',instance.email)
        instance.content=validated_data.get('content',instance.content)
        instance.created=validated_data.get('created',instance.created)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields=(
            'id',
            'title',
            'author',
            'body',
            'slug',
            'created',
        )
        model=models.Post