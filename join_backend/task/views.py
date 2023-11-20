from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer, ContactSerializer, CategorySerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from .models import CustomUser, Contact, Category, Task
from django.db.models.functions import Lower
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'color': user.color,
            'initials': user.initials,
            'user_name': user.user_name,
            'phone': user.phone,
            'user_contact': user.user_contact
            }, status=status.HTTP_200_OK)
        
            else:
                return Response({'details': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': 'User successfull created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "successfully logged out."}, status=status.HTTP_200_OK)
    
class UserView(APIView):
  
    
    def get(self, request):
        users = CustomUser.objects.all().order_by(Lower('user_name'))
        serializer = UserSerializer(users, many=True)  
        return Response(serializer.data)
    
class ContactView(APIView):

    def post(self, request):
        
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exists() or Contact.objects.filter(email=email).exists():
            return Response({'email': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['created_by'] = request.user.id
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, contact_id=None ):

        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class EditContactView(APIView):
    
    def put(self, contact_id):
        email = request.data.get('email')
        contact = Contact.objects.get(id = contact_id)
        if  contact.email != email:
            if CustomUser.objects.filter(email=email).exists() or Contact.objects.filter(email=email).exists():
                return Response({'email': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
        
        if contact is None:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContactSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteContactView(APIView):


    def delete(self, contact_id):
        contact = get_object_or_404(Contact, id=contact_id)
        contact.delete()
        return Response({'detail': 'Contact successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    

class CategoryView(APIView):
    
    def post(self, request):
        
        title = request.data.get('title')
        if Category.objects.filter(title=title).exists():
            return Response({'detail': 'Title already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)  
        return Response(serializer.data)
    
    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response({'detail': 'Category successfully deleted.'},status=status.HTTP_204_NO_CONTENT)
    
class TaskView(APIView):
        
    def post(self, request):
        
        title = request.data.get('title')
        if Task.objects.filter(title=title).exists():
            return Response({'detail': 'Title already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TaskSerializer(data = request.data)
        if  serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Task successfully created.', **serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        try:
            task = Task.objects.get(id=request.data.get('id')  )
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        task = get_object_or_404(Task, id=id)
        task.delete()
        return Response({'detail': 'Task successfully deleted.'},status=status.HTTP_204_NO_CONTENT)
        

        
        
    
    

            
        
        
        
        
    
        
       
            
        
        
    
            