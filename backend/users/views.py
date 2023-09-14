import time

from django.core.cache import cache
from django.core.cache import caches
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import UserProfile,UserPermission,OauthProfile,Address
import json
from hashlib import md5
import jwt
from django.conf import settings
import random
import base64
from django.core.mail import send_mail
from utils.logging_dec import logging_check
from carts.views import CartsView
from google.oauth2 import id_token
from google.auth.transport import requests
# Create your views here.

CARTS_CACHE = caches['carts']
carts = CartsView()

def send_active_email(rec,username,verify_url):
    """
    發送激活用驗證信
    :param rec:收件信箱
    :param username:用戶名
    :param verify_url: 驗證網址 由get_verify_url獲取
    :return:
    """
    send_mail(
        subject='miumiushop用戶驗證',
        html_message='''
        尊敬的%s您好,請點擊下方鏈結完成用戶驗證<br>
        <a href='%s'>點擊此處驗證用戶</a><br>
        如無法點擊此連結請複製下列網址並將其貼在您的瀏覽器中<br>
        %s <br>
        <br>
        <br>
        
        感謝您 <br>
        miumiushop 敬上
        '''%(username,verify_url,verify_url),
        from_email='hugoliu82@gmail.com',
        recipient_list=[rec],
        message='',
    )

def send_verify_email(rec,username,verify_number):
    """
    發送6碼驗證碼到信箱
    :param rec: 收件信箱
    :param username: 用戶名
    :return:
    """
    send_mail(
        subject='miumiushop用戶找回密碼',
        html_message='''
            親愛的%s您好,這是您的驗證碼:<br>
            <h1 style="color:red;">%s</h1>
            <br>
            <br>
            請勿將驗證碼洩漏給別人,並請您於10分鐘內儘速驗證<br>
            如這不是您請求的驗證信,請無須理會

            感謝您 <br>
            miumiushop 敬上
            ''' % (username, verify_number),
        from_email='hugoliu82@gmail.com',
        recipient_list=[rec],
        message='',
    )


def get_six_verify_number(email):
    """
    獲取6位數的驗證碼並存入redis
    :param email:
    :return:
    """
    n=1
    code_number = random.randint(100000,999999)
    print(code_number)
    expire_key = f'expire_findpass_{email}'
    # 限時2分鐘 才能再次要求發送驗證信 避免過於頻繁
    verify_code = cache.get(expire_key)
    if verify_code:
        return 313,code_number
    cache.set(expire_key,code_number,60*2)
    while n<=5:
        daily_expire_key = f'expire_findpass_{email}_{n}'
        daily_expire_code = cache.get(daily_expire_key)
        if daily_expire_code:
            n+=1
            continue
        else:
            cache.set(daily_expire_key,n,86400)
            break
    else:
        return 314,code_number

    key = f'findpass_{email}'
    cache.set(key,code_number,60*10)
    return 200,code_number




def get_verify_url(email):
    """
    獲取激活郵件網址
    :param email:
    :return:
    """
    code_number = random.randint(1000,9999)
    code_string = f'{code_number}_{email}'
    code = base64.urlsafe_b64encode(code_string.encode()).decode()
    verify_url = f'http://127.0.0.1:7001/miumiushop/site/active.html?code={code}'
    key = f'email_active_{email}'
    cache.set(key,code_number,3600*24)
    return verify_url

def make_token(email,exp=86400):
    """
    創建用戶token
    :param email:
    :param exp:
    :return:
    """
    payload = {
        'exp':time.time()+exp,
        'email':email
    }
    key = settings.JWT_TOKEN_KEY
    return jwt.encode(payload,key,algorithm='HS256')


def get_md5_password(password):
    """
    獲取md5加密密碼
    :param password:原始密碼
    :return: md5加密後的密碼
    """
    m = md5()
    m.update(password.encode())
    return m.hexdigest()

class UserViews(View):

    def post(self,request):

        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_check = data.get('password_check')
        gender_num = data.get('gender')
        birthday = data.get('birthday')
        phone = data.get('phone')
        print(data)

        # 判斷提交內容是否完整
        if not username or not email or not password or not password_check or not birthday or not phone:
            return JsonResponse({'code':10301,'error':'提交內容不能為空'})
        # 判斷信箱是否已註冊
        old_user = UserProfile.objects.filter(email=email)
        if old_user:
            return JsonResponse({'code':10302,'error':'該信箱已被註冊'})
        # 判斷密碼與確認密碼是否一致
        if password != password_check:
            return JsonResponse({'code':10303,'error':'兩次密碼不一致'})

        # 將密碼以md5加密
        pwd_md5 = get_md5_password(password)
        # 默認為一般會員
        user_permission = UserPermission.objects.get(permission_num=1)
        # 判斷性別
        if gender_num == '1':
            gender = 'M'
        elif gender_num == '2':
            gender = 'F'
        else:
            gender = 'Unknown'


        # 創建用戶
        try:
            user = UserProfile.objects.create(username=username,
                                              email=email,
                                              password=pwd_md5,
                                              gender=gender,
                                              birthday=birthday,
                                              phone=phone,
                                              user_permission=user_permission)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10304,'error':'創建失敗,請重試'})

        token = make_token(email)
        res = {
            'code':200,
            'email':email,
            'username':username,
            'data':{'token':token},

        }
        # 發送驗證信
        verify_url = get_verify_url(email)
        send_active_email(user.email,user.username,verify_url)

        return JsonResponse(res)



def active_view(request):
    """
    用戶信箱驗證
    :param request:
    :return:
    """
    code = request.GET.get('code')
    code_string = base64.urlsafe_b64decode(code.encode()).decode()
    verify,email = code_string.split('_')
    key = f'email_active_{email}'
    print('key:',key)
    redis_verify = str(cache.get(key))
    print('redis_verify:',redis_verify)
    # str將None轉換程'None'所以這邊判斷必須是'None'
    if redis_verify=='None':
        return JsonResponse({'code':10305,'error':'驗證碼已過期，請重新發送驗證信'})
    if redis_verify != verify:
        return JsonResponse({'code':10306,'error':'驗證失敗'})
    try:
        user = UserProfile.objects.get(email=email)
    except Exception as e:
        print(e)
        return JsonResponse({'code':10307,'error':'該用戶不存在'})
    user.is_active = True
    user.save()
    cache.delete(key)
    return JsonResponse({'code':200,'data':'驗證成功'})


def check_active_view(request,email):
    """
    確認用戶是否驗證(驗證頁)
    :param request:
    :param email:
    :return:
    """
    try:
        user = UserProfile.objects.get(email=email)
    except Exception as e:
        print(e)
        return JsonResponse({'code':10308,'error':'此信箱尚未註冊'})
    if user.is_active == True:
        return JsonResponse({'code':200,'data':'OK'})
    else:
        return JsonResponse({'code':10309,'error':'尚未驗證'})


def login_view(request):
    """
    用戶登入
    :param request:
    :return:
    """
    data = json.loads(request.body)
    print(data)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({'code':10310,'error':'請填寫完整的帳號及密碼'})
    try:
        user = UserProfile.objects.get(email=email)
    except Exception as e:
        print(e)
        return JsonResponse({'code':10308,'error':'此信箱尚未註冊'})
    # 獲取md5加密密碼進行比對
    pwd_md5 = get_md5_password(password)
    if pwd_md5 != user.password:
        return JsonResponse({'code':10311,'error':'密碼錯誤'})

    token = make_token(email)
    carts_dict = carts.get_carts_dict(user.id)

    res = {
        'code': 200,
        'email': email,
        'username': user.username,
        'data': {'token': token},
        'carts_count':len((carts_dict))
    }
    return JsonResponse(res)

def forget_password_getverify_view(request):
    """
    用戶忘記密碼
    1.輸入email發送驗證信
    2.輸入6碼驗證碼
    3.輸入新密碼及確認密碼進行修改
    :param request:
    :return:
    """
    data = json.loads(request.body)
    email = data.get('email')

    if not email:
        return JsonResponse({'code':10312,'error':'請輸入註冊所用信箱'})
    try:
        user = UserProfile.objects.get(email=email)
    except Exception as e:
        print(e)
        return JsonResponse({'code':10308,'error':'此信箱尚未註冊'})






    code,verify_number = get_six_verify_number(email)
    if code == 200:
        send_verify_email(email,user.username,verify_number)
        return JsonResponse({'code':200,'data':'發送成功'})
    elif code == 313:
        return JsonResponse({'code': 10313, 'error': '發送過於頻繁，請稍後再試'})
    elif code == 314:
        return JsonResponse({'code': 10314, 'error': '請求超過次數，請於24小時後再次請求'})



def check_verify_view(request):
    """
    確認驗證碼是否與寄出的驗證碼相同
    1.確認驗證碼
    2.刪除redis中的驗證碼
    :param request:
    :return:
    """
    data = json.loads(request.body)
    verify = data.get('verify') #str類型
    email = data.get('email')
    print(data)

    if not verify:
        return JsonResponse({'code':10315,'error':'請輸入驗證碼'})

    key = f'findpass_{email}'
    code_number = str(cache.get(key))

    if not code_number:
        return JsonResponse({'code':10316,'error':'驗證碼已過期，請重新獲取'})
    if verify != code_number:
        return JsonResponse({'code':10317,'error':'驗證碼錯誤'})
    cache.delete(key)
    return JsonResponse({'code':200,'data':'驗證碼正確'})

def update_password_view(request):
    """
    更改新密碼
    確認新密碼與確認新密碼是否一致 然後更新資料庫的數據
    :param request:
    :return:
    """
    data = json.loads(request.body)
    email = data.get('email')
    pass1 = data.get('new_pass')
    pass2 = data.get('new_pass_check')
    print(data)

    if not pass1 or not pass2:
        return JsonResponse({'code':10301,'error':'提交內容不能為空'})
    if pass1 != pass2:
        return JsonResponse({'code':10303,'error':'兩次密碼不一致'})
    try:
        user = UserProfile.objects.get(email=email)
    except Exception as e:
        print(e)
        return JsonResponse({'code':10318,'error':'系統異常，請重新操作'})
    md5_newpass = get_md5_password(pass1)
    user.password = md5_newpass
    user.save()
    return JsonResponse({'code':200,'data':'密碼更新成功！'})

class ChangePassword(View):
    @logging_check
    def post(self,request,email):
        """
        在登入狀態下更改用戶密碼
        1.需要登入驗證
        2.獲取舊密碼 新密碼 新密碼確認
        3.更改用戶密碼並保存
        :param request:
        :return:
        """
        data = json.loads(request.body)
        old_pass = data.get('old_pass')
        new_pass = data.get('new_pass')
        new_pass1 = data.get('new_pass_check')
        print(data)

        if not old_pass or not new_pass or not new_pass1:
            return JsonResponse({'code':10301,'error':'提交內容不能為空'})

        try:
            user = UserProfile.objects.get(email=email)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10318,'error':'系統異常，請重新操作'})

        oldpwd_md5 = get_md5_password(old_pass)
        if oldpwd_md5 != user.password:
            return JsonResponse({'code':10319,'error':'舊密碼錯誤'})
        if new_pass != new_pass1:
            return JsonResponse({'code':10303,'error':'兩次密碼不一致'})
        newpwd_md5 = get_md5_password(new_pass)
        user.password = newpwd_md5
        user.save()
        return JsonResponse({'code':200,'data':'變更密碼成功'})


class GoogleOauthToken(View):
    """
    從Google第三方登入獲取資料
    1.確認數據
    2.查詢uid是否已存在:
        已存在:簽發token並讓用戶登入
        不存在:利用email判斷是否已經是本站會員:
            是本站會員:OauthProfile綁定user 簽發token
            不是本站會員:註冊UserProfile&OauthProfile 簽發token 發送驗證信
    """
    def post(self,request):
        data = json.loads(request.body)
        print(data)
        uid = data.get('uid')
        username = data.get('username')
        email = data.get('email')

        if not uid or not username or not email:
            return JsonResponse({'code':10320,'error':'獲取資料失敗，請再試一次'})
        # 查詢uid確認是否已經是本站會員且第三方綁定
        try:
            google_user = OauthProfile.objects.get(provider='Google',userID=uid)
        # 沒查到uid 查詢email確認是否是本站會員
        except Exception as e:
            user = UserProfile.objects.filter(email=email)
            # email存在:是本站會員 給用戶綁定Oauthprofile 然後簽發token
            if user:
                user = user[0]
                g_user = OauthProfile.objects.create(provider='Google',userID=uid,userprofile=user)
                token = make_token(user.email)
                carts_dict = carts.get_carts_dict(user.id)
                res = {
                    'code': 200,
                    'email': user.email,
                    'username': user.username,
                    'data': {'token': token},
                    'carts_count': len((carts_dict))
                }
                return JsonResponse(res)
            # email不存在:不是本站會員 創建user用戶並綁定Oauthprofile 後簽發token
            user_permission = UserPermission.objects.get(permission_num=1)
            user = UserProfile.objects.create(username=username,email=email,user_permission=user_permission)
            g_user = OauthProfile.objects.create(provider='Google',userID=uid,userprofile=user)
            token = make_token(email)
            carts_dict = carts.get_carts_dict(user.id)
            res = {
                'code': 201, #第一次註冊尚未驗證
                'email': email,
                'username': username,
                'data': {'token': token},
                'carts_count': len((carts_dict))
            }
            print(res)
            # 發送驗證信
            verify_url = get_verify_url(email)
            send_active_email(user.email, user.username, verify_url)
            return JsonResponse(res)
        email = google_user.userprofile.email
        username = google_user.userprofile.username
        user_id = google_user.userprofile.id
        token = make_token(email)
        carts_dict = carts.get_carts_dict(user_id)
        res = {
            'code': 200,
            'email': email,
            'username': username,
            'data': {'token': token},
            'carts_count': len((carts_dict))
        }
        print(res)
        return JsonResponse(res)


class FbOauthToken(View):
    """
    從Fb第三方登入獲取資料
    1.確認數據
    2.查詢uid是否已存在:
        已存在:簽發token並讓用戶登入
        不存在:利用email判斷是否已經是本站會員:
            是本站會員:OauthProfile綁定user 簽發token
            不是本站會員:註冊UserProfile&OauthProfile 簽發token 發送驗證信
    """
    def post(self,request):
        data = json.loads(request.body)
        print(data)
        uid = data.get('uid')
        username = data.get('username')
        email = data.get('email')

        if not uid or not username or not email:
            return JsonResponse({'code':10320,'error':'獲取資料失敗，請再試一次'})
        # 查詢uid確認是否已經是本站會員且第三方綁定
        try:
            fb_user = OauthProfile.objects.get(provider='Facebook',userID=uid)
        # 沒查到uid 查詢email確認是否是本站會員
        except Exception as e:
            user = UserProfile.objects.filter(email=email)
            # email存在:是本站會員 給用戶綁定Oauthprofile 然後簽發token
            if user:
                user = user[0]
                f_user = OauthProfile.objects.create(provider='Facebook',userID=uid,userprofile=user)
                token = make_token(user.email)
                carts_dict = carts.get_carts_dict(user.id)
                res = {
                    'code': 200,
                    'email': user.email,
                    'username': user.username,
                    'data': {'token': token},
                    'carts_count': len((carts_dict))
                }
                return JsonResponse(res)
            # email不存在:不是本站會員 創建user用戶並綁定Oauthprofile 後簽發token
            user_permission = UserPermission.objects.get(permission_num=1)
            user = UserProfile.objects.create(username=username,email=email,user_permission=user_permission)
            f_user = OauthProfile.objects.create(provider='Facebook',userID=uid,userprofile=user)
            token = make_token(email)
            carts_dict = carts.get_carts_dict(user.id)
            res = {
                'code': 201, #第一次註冊尚未驗證
                'email': email,
                'username': username,
                'data': {'token': token},
                'carts_count': len((carts_dict))
            }
            print(res)
            # 發送驗證信
            verify_url = get_verify_url(email)
            send_active_email(user.email, user.username, verify_url)
            return JsonResponse(res)
        email = fb_user.userprofile.email
        username = fb_user.userprofile.username
        user_id = fb_user.userprofile.id
        token = make_token(email)
        carts_dict = carts.get_carts_dict(user_id)
        res = {
            'code': 200,
            'email': email,
            'username': username,
            'data': {'token': token},
            'carts_count': len((carts_dict))
        }
        print(res)
        return JsonResponse(res)

class Personal_info_View(View):
    """
    獲取個人資訊&地址資訊
    """
    @logging_check
    def get(self,request,email):
        try:
            user = UserProfile.objects.get(email=email)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10318,'error':'系統異常，請重新操作'})
        password = user.password
        if password:
            password = 'exist'
        data = {
            'username':user.username,
            'email':user.email,
            'phone':user.phone,
            'gender':user.gender,
            'birthday':user.birthday,
            'password':password,
            'permission_name':user.user_permission.permission_name,
            'is_active':user.is_active
        }

        all_address = Address.objects.filter(user_profile=user)
        address_data = []
        for address in all_address:
            address_address = address.address
            county = address_address.split('-')[0]
            district = address_address.split('-')[1]
            road = address.address.split('-')[2]
            _dict = {
                'id':address.id,
                'receiver':address.receiver,
                'receiver_phone':address.receiver_phone,
                'county':county,
                'district':district,
                'road':road
            }
            address_data.append(_dict)
        return JsonResponse({'code':200,'userlist':data,'addresslist':address_data})

    @logging_check
    def post(self,request,email):
        """
        建立訂單時添加地址 才用post方法 不然用put
        :param request:
        :param email:
        :return:
        """
        data = json.loads(request.body)
        receiver = data.get('receiver')
        receiver_phone = data.get('receiver_phone')
        county = data.get('county')
        district = data.get('district')
        road = data.get('road')
        user = request.myuser
        address = county+'-'+district+'-'+road
        print(data,address)

        if not receiver or not receiver_phone or not county or not district or not road:
            return JsonResponse({'code': 10323, 'error': '地址表單不能為空'})
        try:
            addr = Address.objects.create(
                receiver=receiver,
                receiver_phone=receiver_phone,
                address=address,
                user_profile=user,
            )
        except Exception as e:
            print(e)
            return JsonResponse({'code':10318,'error':'系統異常，請重新操作'})
        return JsonResponse({'code':200,'data':{'id':addr.id}})

    @logging_check
    def put(self,request,email):
        data = json.loads(request.body)
        username = data.get('username')
        email_user = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        gender_num = data.get('gender')
        birthday = data.get('birthday')

        addressinfo_list = data.get('addressinfo_list')

        print(data)

        # 個人訊息部份
        if email != email_user:
            return JsonResponse({'code':10318,'error':'系統異常，請重新操作'})
        if not email_user or not username:
            return JsonResponse({'code':10321,'error':'用戶名及信箱不能為空'})
        user = UserProfile.objects.get(email=email)
        if user.phone or user.birthday:
            if not phone or not birthday:
                return JsonResponse({'code':10322,'error':'手機及生日不能為空'})

        if gender_num == '1':
            gender = 'M'
        elif gender_num == '2':
            gender = 'F'
        else:
            gender = 'Unknown'

        if password:
            pwd_md5 = get_md5_password(password)
            user.password = pwd_md5
            user.save()

        if not birthday:
            birthday = None
        else:
            y,m,d = birthday.split('-')
            if not y or not m or not d:
                return JsonResponse({'cdoe':10326,'error':'請填寫完整生日'})
        user.username = username
        user.phone = phone
        user.gender = gender
        user.birthday = birthday
        user.save()

        for receiver,receiver_phone,address,address_id in addressinfo_list:
            if receiver or receiver_phone or address:
                if not receiver or not receiver_phone or not address:
                    return JsonResponse({'code':10323,'error':'地址表單不能為空'})
                # 如果有address_id存在代表資料庫中有地址數據:put修改
                #                不存在:post上傳
                try:
                    addr = Address.objects.get(id=address_id,user_profile=user)
                except Exception as e:
                    print(e)
                    addr = Address.objects.create(receiver=receiver,
                                                  receiver_phone=receiver_phone,
                                                  address=address,
                                                  user_profile=user)
                addr.receiver = receiver
                addr.receiver_phone = receiver_phone
                addr.address = address
                addr.save()
        return JsonResponse({'code':200,'data':'OK'})

    @logging_check
    def delete(self,request,email):
        data = json.loads(request.body)
        id = data.get('id')

        print(data)

        user = UserProfile.objects.get(email=email)
        try:
            address = Address.objects.get(id=id,user_profile=user)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10324,'error':'未獲取到地址'})
        try:
            address.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'code':10325,'error':'操作失敗，請再試一次或重新整理'})
        return JsonResponse({'code':200,'data':'OK'})


def info_get_verify_view(request,email):
    """
    用戶重新獲取驗證碼方法 如已驗證就提示已驗證
    :param request:
    :param email:
    :return:
    """
    try:
        user = UserProfile.objects.get(email=email)
    except Exception as e:
        print(e)
        return JsonResponse({'code':10318,'error':'系統異常，請重新操作'})
    username = user.username
    is_active = user.is_active
    if is_active:
        return JsonResponse({'code':10325,'error':'用戶已驗證，不需再次驗證'})
    else:
        verify_url = get_verify_url(email)
        send_active_email(email,username,verify_url)
        return JsonResponse({'code':200,'data':'OK'})











