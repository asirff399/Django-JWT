from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_class = AllowAny
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_serializer = UserSerializer(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': user_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {'message': 'Invalid credentials. Please try again.'},
                    status=status.HTTP_401_UNAUTHORIZED,)
        except User.DoesNotExist:
            return Response(
                {'message': 'User with this email does not exist.'},
                status=status.HTTP_404_NOT_FOUND,)
        
class DashboardView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            'message':'Welcome to Dashboard',
            'user':user_serializer.data
        },status=status.HTTP_200_OK)