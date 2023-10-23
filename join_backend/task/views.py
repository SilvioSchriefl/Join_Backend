from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import LoginSerializer

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
            }, status=status.HTTP_200_OK)
        
            else:
                return Response({'details': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)