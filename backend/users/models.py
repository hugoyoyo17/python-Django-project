from django.db import models

# Create your models here.

class UserPermission(models.Model):
    permission_num = models.IntegerField()
    permission_name = models.CharField(max_length=8)

class UserProfile(models.Model):
    """
    用戶表
    """
    # 用戶名、電子信箱、密碼、性別、生日、聯絡電話、是否激活、创建时间、更新时间
    username = models.CharField(max_length=11,verbose_name='用戶名')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=32,null=True)
    gender = models.CharField(max_length=7,null=True)
    birthday = models.DateField(null=True)
    phone = models.CharField(max_length=10,null=True)
    user_permission = models.ForeignKey(UserPermission,on_delete=models.CASCADE)

    is_active = models.BooleanField(default=False,verbose_name='是否激活')
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_user_profile"

class OauthProfile(models.Model):
    provider = models.CharField(max_length=10)
    userID = models.CharField(max_length=30)
    userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_oauth_profile'

class Address(models.Model):
    receiver = models.CharField('收件人',max_length=10)
    receiver_phone = models.CharField('收件人手機',max_length=10)
    address = models.CharField('收件地址',max_length=50)
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_address'



