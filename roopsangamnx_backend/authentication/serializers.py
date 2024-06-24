from rest_framework import serializers
from .models import RSGUser as User, ShopOwner, BillingDesk, Scanner

class RSGUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ShopOwnerSerializer(serializers.ModelSerializer):
    user = RSGUserSerializer()

    class Meta:
        model = ShopOwner
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, user_type='shopowner')
        shop_owner = ShopOwner.objects.create(user=user, **validated_data)
        return shop_owner
    
    def get_user_type(self, instance):
        return instance.user.user_type


class BillingDeskSerializer(serializers.ModelSerializer):
    user = RSGUserSerializer()

    class Meta:
        model = BillingDesk
        fields = "__all__"

    def to_representation(self, instance):
        # Accessing the request object from the context
        assigned_shop = self.context.get('assigned_shop', None)
        print("s",assigned_shop)

        return super().to_representation(instance)

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        user_serializer = RSGUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(user_type='billingdesk')
        billing_desk = BillingDesk.objects.create(user=user, **validated_data)
        return billing_desk
    
    def get_user_type(self, instance):
        return instance.user.user_type


class ScannerSerializer(serializers.ModelSerializer):
    user = RSGUserSerializer()

    class Meta:
        model = Scanner
        fields = ['user', 'assigned_desk']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = RSGUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(user_type='scanner')
        scanner = BillingDesk.objects.create(user=user, **validated_data)
        return scanner 
    
    def get_user_type(self, instance):
        return instance.user.user_type
