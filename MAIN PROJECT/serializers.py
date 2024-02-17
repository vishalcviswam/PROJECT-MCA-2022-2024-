from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import NormalUser

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_normal_user=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class NormalUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = NormalUser
        fields = ('user', 'first_name', 'last_name', 'phone_number', 'country', 'gender', 'profile_photo', 'cover_photo', 'about_me')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        normal_user = NormalUser.objects.create(user=user, **validated_data)
        return normal_user
