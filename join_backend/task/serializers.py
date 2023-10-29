from rest_framework import serializers
from .models import CustomUser, Contact, Category


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'color', 'initials', 'user_name', 'phone', 'contact')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Passwort sicher hashen
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class UserSerializer(serializers.ModelSerializer):
    
   class Meta:
        model = CustomUser
        fields = ('email', 'color', 'initials', 'user_name', 'id', 'phone', 'contact')
        
class ContactSerializer(serializers.ModelSerializer):
    
   class Meta:
        model = Contact
        fields = ('email', 'color', 'initials', 'user_name', 'id', 'phone' ,'contact')
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('title', 'color', 'id')
        


