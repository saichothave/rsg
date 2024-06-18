from django.contrib.auth.models import User
from rest_framework import serializers

class RSGUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()