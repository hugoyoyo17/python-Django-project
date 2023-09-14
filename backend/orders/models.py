from django.db import models

from goods.models import SKU
from users.models import UserProfile

# Create your models here.


STATUS_CHOICES = (
    (0, '已取消'),
    (1, '待付款'),
    (2, '待發貨'),
    (3, '待收貨'),
    (4, '訂單完成'),
)

class OrderInfo(models.Model):
    """
    訂單表
    用戶表:訂單表 1:n
    訂單編號 訂單總金額 支付方式 運費 訂單狀態 收穫地址等相關字段
    """
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=64,primary_key=True,verbose_name='訂單編號')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='訂單總金額')
    total_count = models.IntegerField(verbose_name='商品總數')
    pay_method = models.SmallIntegerField(default=1,verbose_name='支付方式')
    freight = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='運費')
    status = models.SmallIntegerField(verbose_name='訂單狀態',choices=STATUS_CHOICES)

    receiver = models.CharField(max_length=10,verbose_name='收件人')
    receiver_phone = models.CharField(max_length=10,verbose_name='收件人手機')
    address = models.CharField(max_length=100,verbose_name='收件地址')
    remark = models.TextField(verbose_name='商品備註')

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders_order_info'
        verbose_name = '訂單訊息'
        verbose_name_plural = verbose_name

class OrderGoods(models.Model):
    """
    訂單商品表
    訂單表:訂單商品表 1:n
    SKU:訂單商品表 1:n
    """
    order_info = models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU,on_delete=models.CASCADE)

    # 數量 價格
    count = models.IntegerField(default=1,verbose_name='數量')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='單價')

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders_order_goods'