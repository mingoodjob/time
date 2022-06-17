from venv import create
from django.contrib.auth import login, logout, authenticate
from pytz import timezone
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from blog.models import Category, Article 
from user.models import UserModel, UserType, UserLog
from datetime import datetime, timezone

class UserApiView(APIView):
    
    def get(self, request):
        return Response({'message': '겟!'})
 
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            useremail = UserModel.objects.get(email=email)
            date = datetime.now()
            print(f'메일 : {useremail} 시간 : {date}')
            userlog = UserLog.objects.create(useremail=useremail, login_date=date)
            return Response({'message': '로그인 성공'})
        return Response({'message': '로그인 실패'})
    
    def delete(self, request):
        #로그아웃
        logout(request)
        
class UserSignUp(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user_type = request.data.get('user_type')

        UserModel.objects.create(email=email, password=password, user_type=user_type)

        return Response({'message': '회원가입 성공'})

        
