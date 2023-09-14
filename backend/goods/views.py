import json
import random

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import *
from utils.cache_check import cache_check

# Create your views here.



def get_sku_sales_number():
    """
    獲取sku庫存與銷量 (但只限於有出庫過的！）
    :return:
    """
    stock_list = Stock.objects.all()
    result = []
    for r in range(len(stock_list)):
        same_product = []
        for c in range(r+1,len(stock_list)-1):
            if stock_list[r].sku_id == stock_list[c].sku_id:
                # same_product.append(stock_list[r])
                # same_product.append(stock_list[c])
                stock = 0
                sales = 0
                if stock_list[r].storage_in_out == '入庫':
                    stock += stock_list[r].quantity
                if stock_list[r].storage_in_out == '出庫':
                    stock -= stock_list[r].quantity
                    sales += stock_list[r].quantity
                if stock_list[c].storage_in_out == '入庫':
                    stock += stock_list[c].quantity
                if stock_list[c].storage_in_out == '出庫':
                    stock -= stock_list[c].quantity
                    sales += stock_list[c].quantity
                skuid = f'sku_id:{stock_list[r].sku_id}'
                stock_list[r].sku.sales = sales
                stock_list[r].sku.save()
                same_product.append(skuid)
                same_product.append(stock)
                same_product.append(sales)
        result.append(same_product)
    print(result)
    return

def get_spu_sales_number():
    """
    獲取所有sku加總的spu銷量
    :return:
    """
    spu_list = SPU.objects.all()
    for spu in spu_list:
        spu_sales = 0
        sku_list = SKU.objects.filter(spu=spu)
        for sku in sku_list:
            spu_sales += sku.sales
        print(spu_sales)
        spu.sales = spu_sales
        spu.save()

    return


class GoodsIndexView(View):
    def get(self,request):
        """
        從mysql獲取數據
        需求:
        取出3個銷量最多的商品
        取出3個狗狗商品
        取出3個貓貓商品
        :param request:
        :return:
        """
        # 獲取所有狗狗商品並隨機取3個
        dog_catalog = Catalog.objects.filter(product_for='狗')
        all_product = []
        for cata in dog_catalog:
            spu_list = SPU.objects.filter(catalog=cata)

            for spu in spu_list:
                sku = SKU.objects.filter(spu=spu,is_launched=True)
                spu_dict = {

                    'spuid':spu.id,
                    'name':spu.name,
                    'caption':sku[0].caption,
                    'price':sku[0].cost_price,
                    'image':str(sku[0].default_image_url)
                }
                all_product.append(spu_dict)

        while True:
            index1 = random.randint(0,len(all_product)-1)
            index2 = random.randint(0,len(all_product)-1)
            index3 = random.randint(0,len(all_product)-1)
            if index1 != index2 and index1 != index3 and index2 != index3:
                break

        data_dog = []
        data_dog.append(all_product[index1])
        data_dog.append(all_product[index2])
        data_dog.append(all_product[index3])
        print(data_dog)


        # 獲取貓咪商品並隨機選3個
        cat_catalog = Catalog.objects.filter(product_for='貓')
        all_product = []
        for cata in cat_catalog:
            spu_list = SPU.objects.filter(catalog=cata)

            for spu in spu_list:
                sku = SKU.objects.filter(spu=spu,is_launched=True)
                spu_dict = {
                    'spuid':spu.id,
                    'name':spu.name,
                    'caption':sku[0].caption,
                    'price':sku[0].cost_price,
                    'image':str(sku[0].default_image_url)
                }
                all_product.append(spu_dict)

        while True:
            index1 = random.randint(0,len(all_product)-1)
            index2 = random.randint(0,len(all_product)-1)
            index3 = random.randint(0,len(all_product)-1)
            if index1 != index2 and index1 != index3 and index2 != index3:
                break

        data_cat = []
        data_cat.append(all_product[index1])
        data_cat.append(all_product[index2])
        data_cat.append(all_product[index3])
        print(data_cat)


        # 利用銷量排序後 取前3
        all_product = []
        spu_list = SPU.objects.all().order_by('-sales')[:3]
        for spu in spu_list:
            sku = SKU.objects.filter(spu=spu,is_launched=True)
            spu_dict = {
                'spuid':spu.id,
                'name':spu.name,
                'caption':sku[0].caption,
                'price':sku[0].cost_price,
                'image':str(sku[0].default_image_url),
                'sales':spu.sales
            }
            all_product.append(spu_dict)

        print(all_product)
        print('獲取mysql數據成功')

        # get_sku_sales_number()
        # get_spu_sales_number()

        return JsonResponse({
                "code": 200,
                "base_url": settings.PIC_URL,
                "data_dog": data_dog,
                'data_cat':data_cat,
                'data_popular':all_product
            })

class GoodsDetailView(View):
    """
    商品詳情頁
    """
    @cache_check(key_prefix='gd',key_param=None,cache='goods_detail',expire=300)
    def get(self,request,spu_id):
        try:
            spu = SPU.objects.get(id=spu_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10401,'error':'獲取商品失敗'})
        data = {}
        spu_catalog = spu.catalog
        sku_list = SKU.objects.filter(spu=spu,is_launched=True)

        # 商品類別
        data['catalog_id'] = spu_catalog.id
        data['catalog_name'] = spu_catalog.name
        data['product_for'] = spu_catalog.product_for
        # 商品名稱
        data['name'] = spu.name
        data['image'] = str(sku_list[0].default_image_url)
        data['price'] = sku_list[0].cost_price
        data['stock'] = sku_list[0].stock_number
        data['caption'] = [sku.caption for sku in sku_list]
        data['spu'] = spu.id

        # 銷售屬性名稱
        res = SPUSaleAttr.objects.filter(spu=spu)
        data['sku_sale_attr_id'] = [r.id for r in res]
        data['sku_sale_attr_name'] = [r.name for r in res]

        # 先求出默認(第一個)SKU的銷售屬性值<QuerySet>
        sku1_sale_attr_values = sku_list[0].sale_attr_value.all()
        data['sku_sale_attr_val_id'] = [sku1_sale_attr_value1.id for sku1_sale_attr_value1 in sku1_sale_attr_values]
        data['sku_sale_attr_val_name'] = [sku1_sale_attr_value1.name for sku1_sale_attr_value1 in sku1_sale_attr_values]


        #  求該SPU所有銷售屬性值
        # 獲取spu中所有銷售屬性名稱對象
        sku_all_sale_attr_vals_id = {}
        sku_all_sale_attr_vals_name = {}
        res = SPUSaleAttr.objects.filter(spu=spu)
        # 獲取spu中所有銷售屬性的id
        attr_id_list = [r.id for r in res]
        print(attr_id_list)
        for attr_id in attr_id_list:
            items = SaleAttrValue.objects.filter(spu_sale_attr=attr_id)
            sku_all_sale_attr_vals_id[attr_id] = [i.id for i in items]
            sku_all_sale_attr_vals_name[attr_id] = [i.name for i in items]
        data['sku_all_sale_attr_vals_id'] = sku_all_sale_attr_vals_id
        data['sku_all_sale_attr_vals_name'] = sku_all_sale_attr_vals_name



        #
        # result2 = []
        # # [QuerySet1,QuerySet2,QuerySet3]
        # res = [sku.sale_attr_value.all() for sku in sku_list]
        # for r in res:
        #     for c in r:
        #         result2.append(c.name)
        # print('res2:',result2)

        res = SKUImage.objects.filter(sku=sku_list[0])
        data['detail_image'] = res[0].image if res else ''

        table = {}
        table['商品說明'] = spu.product_description
        table['商品成份'] = spu.nutrition_facts
        table['商品規格'] = [sku.caption for sku in sku_list]
        table['適用對象'] = spu.apply_to
        table['商品備註'] = spu.remark

        data['table'] = table

        print(data)
        return JsonResponse({
            'code':200,
            'base_url':settings.PIC_URL,
            'data':data
        })
    def post(self,request):
        """
        詳情頁切換SKU
        :param request:
        :return:
        """
        data = json.loads(request.body)
        sale_attr_value_id = data.get('sale_attr_value_id')
        spu_id = data.get('spu_id')
        print(data)

        try:
            sku_sale_attr_value = SaleAttrValue.objects.get(id=sale_attr_value_id)
            sku_list = SKU.objects.filter(sale_attr_value=sku_sale_attr_value,is_launched=True)

        except Exception as e:
            print(e)
            return JsonResponse({'code':10401,'error':'系統異常'})
        for sku in sku_list:
            print(sku.spu.id)
            if str(sku.spu.id) == spu_id:
                data = {
                    'sku_id':sku.id,
                    'caption':sku.caption,
                    'price':sku.cost_price,
                    'image':str(sku.default_image_url),
                    'stock':sku.stock_number
                }
                print(data)
                return JsonResponse({'code':200,
                                     'data':data,
                                     'base_url':settings.PIC_URL
                                     })
            else:
                continue
        return JsonResponse({'code': 10401, 'error': '系統異常'})


class GoodsListView(View):
    """
    商品列表頁
    """
    def get(self,request):
        list_for = request.GET.get('list_for')
        page_num = request.GET.get('page',1)
        limit = request.GET.get('limit',12)
        if page_num == 'null':
            page_num = 1
        elif type(page_num) != 'int':
            try:
                page_num = int(page_num)
            except Exception as e:
                print(e)
                return JsonResponse({'code':10403,'error':'並無該分頁或分類，請重新查詢'})

        if limit == 'null':
            limit = 12
        elif type(limit) != 'int':
            try:
                limit = int(limit)
            except Exception as e:
                print(e)
                return JsonResponse({'code':10403,'error':'並無該分頁或分類，請重新查詢'})
            if limit > 12:
                limit = 12

        print(list_for,page_num,limit)

        if list_for == '人氣商品':
            spu_list = SPU.objects.all().order_by('-sales')
            # print(spu_list)
            data = []
            for spu in spu_list:
                sku = SKU.objects.filter(spu=spu, is_launched=True)
                dict_ = {
                    'spuid': spu.id,
                    'name': spu.name,
                    'image': str(sku[0].default_image_url),
                    'price': sku[0].cost_price,
                }
                data.append(dict_)
            print(data)

        else:
            product_for = list_for[:-2]
            if product_for == '狗狗':
                product_for= '狗'
            elif product_for == '貓咪':
                product_for = '貓'
            else:
                return JsonResponse({'code':10402,'error':'商品尚未上架，敬請期待'})
            cata = list_for[-2:]
            if cata == '商品':
                cata_products = Catalog.objects.filter(product_for=product_for)

            else:
                cata_products = Catalog.objects.filter(product_for=product_for,name=cata)
            if cata_products:
                data = []
                for cata_product in cata_products:
                    spu_list = SPU.objects.filter(catalog=cata_product)
                    for spu in spu_list:
                        sku = SKU.objects.filter(spu=spu, is_launched=True)
                        dict_ = {
                            'spuid': spu.id,
                            'name': spu.name,
                            'image': str(sku[0].default_image_url),
                            'price': sku[0].cost_price,
                        }
                        data.append(dict_)
                print(data)
            else:
                return JsonResponse({'code':10402,'error':'商品尚未上架，敬請期待'})

        paginator = Paginator(data,limit)
        try:
            page = paginator.page(page_num)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10403,'error':'並無該分頁或分類，請重新查詢'})
        data = {}
        data['objects'] = page.object_list
        data['num_pages'] = paginator.num_pages
        data['type_of'] = list_for
        data['limit'] = limit
        data['page_now'] = page_num
        print(data)

        return JsonResponse({'code':200,'data':data,'base_url':settings.PIC_URL})



