from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from django.contrib.auth import authenticate
from .models import AUser
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }
class UserRegistrationView(APIView):
    def post(self,request,format=None):
        # def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True ):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token},serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserLoginView(APIView):
     def post(self, request, format=None):
       serializer=UserLoginSerializeer(data=request.data)
       if serializer.is_valid(raise_exception=True):
          email=serializer.data.get('email')
          password=serializer.data.get('password')
          user=authenticate(email=email,password=password)
          if user is not None:
              token=get_tokens_for_user(user)
              return Response({"msg":"Login successfull","token":token},status=status.HTTP_200_OK)
          else:
               return Response({"errors":"email or password not valid"},status=status.HTTP_404_NOT_FOUND)
       else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        serializer=UserProfileSerialzer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ChangePasswordView(APIView):
  permission_classes=[IsAuthenticated]
  def post(self, request,fromat=None):
      serializer=ChangePasswordSerializer(data=request.data,context={
          'user':request.user
      })
      if serializer.is_valid(raise_exception=True ):
           return Response({"msg":"successfulll"},status=status.HTTP_200_OK)
      else:
          return Response({"fsdc":"error"},status=status.HTTP_200_OK)
class SendEmailReset(APIView):
    def post(self, request,format=None):
        serializer=SendEmailPasswordSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
              return Response({"msg":"successfulll send email"},status=status.HTTP_200_OK)
        else:
          return Response({"fsdc":"error not send email"},status=status.HTTP_200_OK)
class Userpasswordreset(APIView):       
    def post(self, request,uid,token,format=None):
      serializer=UserPasswordResetSerializer(data=request.data,context={ 'uid':uid,'token':token })
      if serializer.is_valid(raise_exception=True):
              return Response({"msg":"successfulll reset"},status=status.HTTP_200_OK)
      else:
          return Response({"fsdc":"error not reset"},status=status.HTTP_200_OK)
    
class otp(APIView):
     def post(self, request,format=None):
        serializer=OtpGenerator(data=request.data) 
        if serializer.is_valid(raise_exception=True):
              return Response({"msg":"otp sent"},status=status.HTTP_200_OK)
        else:
          return Response({"fsdc":"error not sent otp"},status=status.HTTP_200_OK)
class OtpVerificationView(APIView):
    def post(self, request):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP verified successfully"})
        else:
            return Response({"error": "Invalid OTP"}, status=400)