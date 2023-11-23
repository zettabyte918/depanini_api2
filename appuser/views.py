from django.db import IntegrityError
from .models import AppUser
from .serializers import RegisterRequestSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import LoginRequestSerializer
from rest_framework.authtoken.models import Token

class Login(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request: Request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        if request.user.is_authenticated:
            response = {
                "message": "Already logged in",
            }
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

        user = authenticate(username=username, password=password)

        if user is not None:
            # generate new token
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)

            user = AppUser.objects.get(email=user.email)

            serializer = UserSerializer(user)

            response = {
                "message": "Login Successfull",
                "user": serializer.data,
                "token": token.key,
                "success": True,
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(
                data={"error": "Invalid username or password", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

class RegisterView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Endpoint to register new users.
        """
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            created_user = AppUser.objects.create(
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
            )
            created_user.set_password(serializer.validated_data.get("password"))
            created_user.save()

        except IntegrityError:
            return Response(
                data="The email address you've selected is already in use."
            )

        result = UserSerializer(created_user)
        return Response(data=result.data)