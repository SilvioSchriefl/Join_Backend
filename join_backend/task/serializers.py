from rest_framework import serializers
from .models import CustomUser, Contact, Category, Task


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
        
        
class TaskSerializer(serializers.ModelSerializer):
    custom_users = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())
    contacts = serializers.PrimaryKeyRelatedField(many=True, queryset=Contact.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Korrekte Verwendung von Category

    class Meta:
        model = Task
        fields = '__all__'


