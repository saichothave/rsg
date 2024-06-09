from django.contrib.auth.models import User
from rest_framework import serializers

class RSGUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)        
        user = User(**validated_data)

        if password is not None:
            user.set_password(password)

        user.save()
        
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()