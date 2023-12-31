# Generated by Django 4.1.2 on 2023-05-24 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='商品名稱')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '品牌',
                'verbose_name_plural': '品牌',
                'db_table': 'goods_brand',
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='類別名稱')),
                ('product_for', models.CharField(max_length=10, verbose_name='商品對象')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '商品類別',
                'verbose_name_plural': '商品類別',
                'db_table': 'goods_catalog',
            },
        ),
        migrations.CreateModel(
            name='SaleAttrValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='銷售屬性值名稱')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '銷售屬性值',
                'verbose_name_plural': '銷售屬性值',
                'db_table': 'goods_sale_attr_value',
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='SKU名稱')),
                ('caption', models.CharField(max_length=100, verbose_name='副標題')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='單價')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='進價')),
                ('market_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='市場價')),
                ('sales', models.IntegerField(default=0, verbose_name='銷量')),
                ('comments', models.IntegerField(default=0, verbose_name='評價數')),
                ('is_launched', models.BooleanField(default=True, verbose_name='上否上架')),
                ('default_image_uel', models.ImageField(upload_to='', verbose_name='默認圖片')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('sale_attr_value', models.ManyToManyField(to='goods.saleattrvalue')),
            ],
            options={
                'verbose_name': 'SKU表',
                'verbose_name_plural': 'SKU表',
                'db_table': 'goods_sku',
            },
        ),
        migrations.CreateModel(
            name='SPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名稱')),
                ('sales', models.IntegerField(default=0, verbose_name='商品銷量')),
                ('comments', models.IntegerField(default=0, verbose_name='評論數量')),
                ('apply_to', models.CharField(max_length=50, verbose_name='適用對象')),
                ('product_description', models.TextField(verbose_name='商品說明')),
                ('nutrition_facts', models.CharField(max_length=100, verbose_name='營養成份')),
                ('remark', models.CharField(max_length=100, verbose_name='商品備註')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.brand', verbose_name='品牌')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.catalog', verbose_name='商品類別')),
            ],
            options={
                'verbose_name': 'SPU',
                'verbose_name_plural': 'SPU',
                'db_table': 'goods_spu',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_in_out', models.CharField(max_length=5, verbose_name='入庫/出庫')),
                ('person_in_charge', models.CharField(max_length=10, verbose_name='負責人')),
                ('quantity', models.IntegerField(verbose_name='入出貨數量')),
                ('version', models.IntegerField(default=0, verbose_name='庫存版本')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.sku', verbose_name='sku')),
            ],
            options={
                'verbose_name': '庫存整理',
                'verbose_name_plural': '庫存整理',
                'db_table': 'goods_sku_stock',
            },
        ),
        migrations.CreateModel(
            name='SPUSaleAttr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='SPU屬性名稱')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.spu')),
            ],
            options={
                'verbose_name': 'SPU銷售屬性',
                'verbose_name_plural': 'SPU銷售屬性',
                'db_table': 'goods_spu_sale_attr',
            },
        ),
        migrations.CreateModel(
            name='SKUImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sku_images', verbose_name='圖片路徑')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.sku', verbose_name='sku')),
            ],
            options={
                'verbose_name': 'SKU圖片',
                'verbose_name_plural': 'SKU圖片',
                'db_table': 'goods_sku_image',
            },
        ),
        migrations.CreateModel(
            name='SKUComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='評價星數')),
                ('comment_text', models.TextField(verbose_name='顧客評價')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.sku', verbose_name='sku')),
            ],
            options={
                'verbose_name': '顧客評論',
                'verbose_name_plural': '顧客評論',
                'db_table': 'goods_sku_comment',
            },
        ),
        migrations.AddField(
            model_name='sku',
            name='spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.spu'),
        ),
        migrations.AddField(
            model_name='saleattrvalue',
            name='spu_sale_attr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.spusaleattr'),
        ),
    ]
