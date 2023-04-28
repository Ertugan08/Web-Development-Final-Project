from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        return {'token': user.token, }


class CategoriesSerializer(serializers.Serializer):
    name = serializers.CharField()
    photo = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'
        # read_only_fields = ('desc', 'info', 'photo', 'category', 'company')