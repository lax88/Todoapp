from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt
from datetime import datetime, timedelta, timezone

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
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

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data={
            'jwt':token
        }
        return response