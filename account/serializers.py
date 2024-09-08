import random
from rest_framework import serializers
from account.models import AUser
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes,smart_str
from rest_framework.exceptions import ValidationError

from account.utils import send_mails,generate_otp
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta: 
        model=AUser
        fields=["email","name","password","password2","tc"]
        extra_kwargs={
            "password":{"write_only":True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("Both passwords do not match")
        return attrs
    def create(self, validated_data):
        return AUser.objects.create_user(**validated_data)
class UserLoginSerializeer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=AUser
        fields=['email','password']
class UserProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model=AUser
        fields=['id','name','email']
class ChangePasswordSerializer(serializers.Serializer):
   
    new_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        fields=[' new_password','  confirm_password']
    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        user=self.context.get('user')
        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password do not match")
        user.set_password(new_password)
        user.save()
        return attrs
class SendEmailPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self,attrs):
        email=attrs.get('email')
        if AUser.objects.filter(email=email).exists():
            user=AUser.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            print("erfd",token)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print("link",link)
            data={
                'subject':'Reset Your Password',
                'body':'Please go to link below to reset your password \n'+link,
                   'to_email':user.email
               }
            
            send_mails(data)
            return attrs
        else:
            raise ValidationError('You are not registered')
class UserPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    class Meta:
        fields=[' new_password','  confirm_password']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        uid=self.context.get('uid')
        token=self.context.get('token')
        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password do not match")
        id=smart_str(urlsafe_base64_decode(uid))
        user=AUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
           raise ValidationError("token not valid")
        user.set_password(new_password)
        user.save()
        return attrs
class OtpGenerator(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = AUser
        fields = ['email']
    def generate_otp(self):
          return str(random.randint(100000, 999999)) 
    def validate(self, attrs):
        email = attrs.get('email')
        if AUser.objects.filter(email=email).exists():
            user = AUser.objects.get(email=email)
            otp = self.generate_otp()
            user.otp=otp  
            user.save()
            print("otp:", otp)
            data = {
                'subject': 'Your OTP',
                'body': f'Your OTP is {otp}',
                'to_email': user.email
            }
            send_mails(data)
            return attrs
        else:
            raise ValidationError('You are not registered')
class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        if AUser.objects.filter(email=email).exists():
            user = AUser.objects.get(email=email)
            if user.otp != otp:
                raise serializers.ValidationError("Invalid OTP")
            user.otp_verified = True
            user.save()
            return attrs
        else:
            raise ValidationError('You are not registered')