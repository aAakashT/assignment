from rest_framework import serializers
from django.contrib.auth.models  import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class UserLoginSerializer(TokenObtainPairSerializer):
    pass

        