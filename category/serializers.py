from rest_framework import serializers
from .models import Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'