from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .serializers import UserSerializer
from .models import User
import jwt
from datetime import datetime, timedelta, timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    permission_classes= [AllowAny]
    def post(self, request):
        email = request.data['email']
        password = request.data['password'] 

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!!')
        
        payload = {
            'id':user.id,
            'exp':datetime.now(timezone.utc)+timedelta(minutes=60),
            'iat':datetime.now(timezone.utc)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response({'jwt':token}, status=status.HTTP_200_OK)

        response.set_cookie(key='jwt', value=token, httponly=True)

        # response.data={
        #     'jwt':token
        # }
        return response
    
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'users/register.html')

        serializer = UserSerializer(data={'username': username, 'email': email, 'password': password})

        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, "Registration failed. Please check your input.")
            return render(request, 'users/register.html', {'form': serializer.errors})
    else:
        return render(request, 'users/register.html')    
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todo-list')  # Redirect to the todo list view after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')    
