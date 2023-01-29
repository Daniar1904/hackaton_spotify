from rest_framework import serializers
from .models import Sound, Comment, Like, Favorite

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
    owner = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['sound'] = instance.sound.title
        return res

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['like', 'sound']

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['sound'] = instance.sound.title
        if instance.like is True:
            res['like'] = 'Liked'
        else:
            res['like'] = 'Unliked'
        return res

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['owner'] = instance.owner.email
        rep['sound'] = instance.sound.title
        return rep
