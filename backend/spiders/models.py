from django.db import models

# Create your models here.


class LangLangSpiderInfo(models.Model):
    name = models.CharField(max_length=20,verbose_name='寵物名稱')
    gender = models.CharField(max_length=10,verbose_name='寵物性別')
    age = models.CharField(max_length=20,null=True,verbose_name='寵物年齡')
    ligation = models.BooleanField(verbose_name='是否結紮')
    vaccination = models.CharField(max_length=20,verbose_name='預防針',null=True)
    deworming = models.CharField(max_length=20,verbose_name='體內外寄生蟲',null=True)
    personality = models.CharField(max_length=100,verbose_name='個性簡介',null=True)
    be_helped = models.CharField(max_length=10,verbose_name='助養人數')
    introduction = models.TextField(verbose_name='浪浪介紹',null=True)
    image = models.ImageField(verbose_name='浪浪圖片',default=None,upload_to='langlang',max_length=2048)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    src = models.CharField(max_length=200,verbose_name='狗狗連結',null=True)

    class Meta:
        db_table = 'langlang_info'
        verbose_name = '浪浪資訊'
        verbose_name_plural = verbose_name
