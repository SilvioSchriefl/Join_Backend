from rest_framework import serializers
from .models import CustomUser, Contact, Category, Task


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'color', 'initials', 'user_name', 'phone', 'user_contact')

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
        fields = ('email', 'color', 'initials', 'user_name', 'id', 'phone', 'user_contact')
        
class ContactSerializer(serializers.ModelSerializer):
    
    created_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = Contact
        fields = ('email', 'color', 'initials', 'user_name', 'id', 'phone' ,'user_contact', 'created_by')
        
        
class CategorySerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Category
        fields = ('title', 'color', 'id')
        
        
class TaskSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Task
        fields = '__all__'


