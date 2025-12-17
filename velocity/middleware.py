import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        token = request.COOKIES.get('access_token')
        
        if not token:
            return

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = User.objects.filter(id=user_id).first()
            
            if user:
                request.user = user
                
        except jwt.ExpiredSignatureError:
            # Token expired
            pass
        except jwt.DecodeError:
            # Invalid token
            pass
