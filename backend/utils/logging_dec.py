import jwt
from django.conf import settings
from django.http import JsonResponse
from users.models import UserProfile

"""
登入驗證裝飾器
"""

def logging_check(func):
    def wrapper(self,request,*args,**kwargs):
        """
        獲取token
        驗證token
        :param self:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        try:
            # {'exp':xxx,'email':xxx}
            payload = jwt.decode(token,settings.JWT_TOKEN_KEY,algorithms='HS256')
        except Exception as e:
            print(e)
            return JsonResponse({'code':403,'error':'請先登入'})

        email = payload.get('email')
        user = UserProfile.objects.get(email=email)
        request.myuser = user

        return func(self,request,*args,**kwargs)
    return wrapper