from rest_framework import serializers
from category.models import Genre
from .models import Sound, Comment, Like

"""Создаем сериализаторы для наших треков"""

class SoundListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Sound
        fields = ('owner_email', 'singer', 'title', 'file', 'cover', 'category')


class SoundSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Sound
        fields = '__all__'


class SoundDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class UsersCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'sound', 'created_at')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['sound_title'] = instance.post.title
        return repr


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        sound = attrs['sound']
        if user.liked_songs.filter(sound=sound).exists():
            raise serializers.ValidationError('You already liked this song!')
        return attrs