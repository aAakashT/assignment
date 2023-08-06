from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView 
from .serializers import UserSerializer, UserLoginSerializer
from .models import BlacklistedToken
from django.contrib.auth.models import User 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
# Create your views here.



class UserRegistrationView(CreateAPIView):
    authentication_classes = []
    serializer_class = UserSerializer
    queryset =  User.objects.all()
    # print(queryset)
    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['access_token'] = self.access_token
        response.data['refresh_token'] = self.refresh_token
        return response
    
class UserLogInView(TokenObtainPairView):
    authentication_classes = []
    permission_classes = [AllowAny,]
    queryset =  User.objects.all()
    serializer_class = UserLoginSerializer
    print(queryset)
   

class UserLogoutView(APIView):
    authentication_classes = []
    def post(self, requst, *args, **kwargs):
        
        try:
            refresh_token = requst.data['refresh']
            print(refresh_token)
            token = RefreshToken(refresh_token)
            
            BlacklistedToken.objects.create(token=str(token.access_token))
            return Response({'message': 'logout sucessfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
            
# def Testing(requset):
                