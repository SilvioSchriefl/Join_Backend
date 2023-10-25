from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from .models import CustomUser
from django.db.models.functions import Lower

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "successfully logged out."}, status=status.HTTP_200_OK)
    
class UserView(APIView):
    
    def get(self, request):
        users = CustomUser.objects.all().order_by(Lower('user_name'))
        serializer = UserSerializer(users, many=True)  
        return Response(serializer.data)
            