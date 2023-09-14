from django.db import models

# Create your models here.





class Catalog(models.Model):
    """
    商品類別
    product_for:貓/狗
    """
    name = models.CharField(max_length=10,verbose_name='類別名稱')
    product_for = models.CharField(max_length=10,verbose_name='商品對象')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_catalog'
        verbose_name = '商品類別'
        verbose_name_plural = verbose_name

class Brand(models.Model):
    """
    品牌
    """
    name = models.CharField(max_length=20,verbose_name='商品名稱')
    # logo = models.ImageField(verbose_name='Logo圖片',upload_to='brand')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

class SPU(models.Model):
    name = models.CharField(max_length=50,verbose_name='名稱')
    sales = models.IntegerField(default=0,verbose_name='商品銷量')
    comments = models.IntegerField(default=0,verbose_name='評論數量')
    brand = models.ForeignKey(Brand,verbose_name='品牌',on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog,verbose_name='商品類別',on_delete=models.CASCADE)
    apply_to = models.CharField(max_length=50,verbose_name='適用對象')
    product_description = models.TextField(verbose_name='商品說明')
    nutrition_facts = models.TextField(verbose_name='營養成份')
    remark = models.CharField(max_length=100,verbose_name='商品備註')
    storage_method = models.CharField(max_length=100,verbose_name='保存方式',default='')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_spu'
        verbose_name = 'SPU'
        verbose_name_plural = verbose_name

class SPUSaleAttr(models.Model):
    """
    SPU銷售屬性表
    """
    spu = models.ForeignKey(SPU,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,verbose_name='SPU屬性名稱')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_spu_sale_attr'
        verbose_name = 'SPU銷售屬性'
        verbose_name_plural = verbose_name

class SaleAttrValue(models.Model):
    """
    銷售屬性值表
    """
    spu_sale_attr = models.ForeignKey(SPUSaleAttr,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,verbose_name='銷售屬性值名稱')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_sale_attr_value'
        verbose_name = '銷售屬性值'
        verbose_name_plural = verbose_name

class SKU(models.Model):
    """
    SKU
    """
    name = models.CharField(max_length=50,verbose_name='SKU名稱')
    caption = models.CharField(max_length=100,verbose_name='副標題')
    spu = models.ForeignKey(SPU,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='單價')
    cost_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='進價')
    market_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='市場價')
    sales = models.IntegerField(default=0,verbose_name='銷量')
    comments = models.IntegerField(default=0,verbose_name='評價數')
    stock_number = models.IntegerField(default=0,verbose_name='庫存數量')
    is_launched = models.BooleanField(default=True,verbose_name='上否上架')
    default_image_url = models.ImageField(verbose_name='默認圖片',default=None,upload_to='sku')
    sale_attr_value = models.ManyToManyField(SaleAttrValue)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_sku'
        verbose_name = 'SKU表'
        verbose_name_plural = verbose_name

class SKUImage(models.Model):
    """
    SKU圖片
    """
    sku = models.ForeignKey(SKU,on_delete=models.CASCADE,verbose_name='sku')
    image = models.ImageField(verbose_name='圖片路徑',upload_to='sku_images')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_sku_image'
        verbose_name = 'SKU圖片'
        verbose_name_plural = verbose_name


class SKUComment(models.Model):
    """
    顧客評價
    """
    sku = models.ForeignKey(SKU,on_delete=models.CASCADE,verbose_name='sku')
    score = models.IntegerField(verbose_name='評價星數')
    comment_text = models.TextField(verbose_name='顧客評價')
    created_time =models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_sku_comment'
        verbose_name = '顧客評論'
        verbose_name_plural = verbose_name

class Stock(models.Model):
    """
    庫存
    """
    sku = models.ForeignKey(SKU,on_delete=models.CASCADE,verbose_name='sku')
    storage_in_out = models.CharField(max_length=5,verbose_name='入庫/出庫')
    person_in_charge = models.CharField(max_length=10,verbose_name='負責人')
    quantity = models.IntegerField(verbose_name='入出貨數量')
    version = models.IntegerField(default=0,verbose_name='庫存版本')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goods_sku_stock'
        verbose_name = '庫存整理'
        verbose_name_plural = verbose_name