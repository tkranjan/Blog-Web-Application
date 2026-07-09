from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    ProfileUpdateSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import isUser

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg":"User Registred"},status=201)
    
class LoginView(APIView):
    def post(self,request):
        
        identifier = request.data.get("identifier")
        password = request.data.get("password")

        User = get_user_model()


        if "@" in identifier:
            try:
                user_obj = User.objects.get(
                    email = identifier
                )
                username =user_obj.username

            except User.DoesNotExist:
                username = None
        else:
            username = identifier

        user = authenticate(
            username = username,
            password = password,
        )
        if not user:
            return Response({"error":"User doesn't exist or Invalid Credentials"},status=401)
        

        refresh = RefreshToken.for_user(user)

        res = Response({
            "access_token" : str(refresh.access_token)
        })

        #store refresh token in Httponly cookie

        res.set_cookie(
            key = "refresh_token",
            value = str(refresh),
            httponly = True,
            secure = False,
            samesite = "Lax",
            path = "/"
        )
        return res


class RefreshView(APIView):
    def post(self,request):
        token = request.COOKIES.get("refresh_token")
        if not token:
            return Response({"error": "No Refresh Token"},status=401)
        
        try:
            refresh = RefreshToken(token)
            access = str(refresh.access_token)
        except Exception:
            return Response({"error":"Invalid Refresh Token"},status=401)
        

        return Response({"refresh_token":access})
    
class LogoutView(APIView):
    def post(self,request):
        res = Response({"msg":"Logged Out"})
        res.delete_cookie("refresh_token","/api/auth/refresh")
        return res
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({
            "username": request.user.username,
            "role": request.user.role
        })
    
class ProfileUpdateView(APIView):
    permission_classes = [isUser]

    def patch(self,request):
        serializer = ProfileUpdateSerializer(
            request.user,
            data = request.data,
            partial = True        
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors,status=400)

class ForgotPasswordView(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerializer(
            data = request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Password Reset link sent successfully."
                    "Check spam folder if you do not see it in inbox."
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ResetPasswordView(APIView):
    def post(self,request,uidb64,token):
        serializer = ResetPasswordSerializer(
            data = request.data
        )

        if serializer.is_valid():
            serializer.save(uidb64=uidb64,
                            token=token)

            return Response(
                {
                    "message":"Password Reset Successful"
                },
                
                status = status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )

