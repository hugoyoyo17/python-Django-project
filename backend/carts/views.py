import json

from django.conf import settings
from django.core.cache import caches
from django.http import JsonResponse
from django.shortcuts import render
from utils.logging_dec import logging_check
# Create your views here.
from django.views import View
from goods.models import *


CARTS_CACHE = caches['carts']

class CartsView(View):
    @logging_check
    def post(self,request,email):
        """
        添加購物車
        1.獲取請求數據(sku,count)
        2.存入redis
        "carts_userid":{"skuid":[count,selected]}
        "carts_1":{"1":[3,1],"2":[8,0]}
        3.返回響應
        :param request:
        :param email:
        :return:
        """
        data = json.loads(request.body)
        spu_id = data.get('spuid')
        sale_attr_value_id = data.get('sale_attr_value_id')
        count = int(data.get('count'))
        stock_num = int(data.get('stock'))
        print(data)


        if count>stock_num:
            return JsonResponse({'code':10404,'error':'購買數量超過庫存'})

        try:
            sku_sale_attr_value = SaleAttrValue.objects.get(id=sale_attr_value_id)
            sku = SKU.objects.get(sale_attr_value=sku_sale_attr_value,spu__in=spu_id,is_launched=True)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10401,'error':'系統異常'})
        print(sku)

        user = request.myuser
        # 1.查詢購物車所有數據
        carts_dict = self.get_carts_dict(user.id)
        # 加入購物車
        if sku.id not in carts_dict:
            carts_dict[sku.id] = [count, 1]
        else:
            buy_count = carts_dict[sku.id][0]+count
            if buy_count>stock_num:
                return JsonResponse({'code':10405,'error':f'購買數量超過庫存，購物車中已有{carts_dict[sku.id][0]}件'})
            carts_dict[sku.id][0] = buy_count
        # 存入redis
        key = f'carts_{user.id}'
        CARTS_CACHE.set(key,carts_dict)
        # 返回響應
        result = {
            'code':200,
            'data':{'carts_count':len(carts_dict)},
            'base_url':settings.PIC_URL
        }
        return JsonResponse(result)

    @logging_check
    def get(self,request,email):
        """
        查詢購物車
        :param request:
        :return:
        """
        user = request.myuser
        skus_list = self.get_skus_list(user.id)
        
        result = {
            'code':200,
            'data':skus_list,
            'base_url':settings.PIC_URL
        }
        print(skus_list)
        return JsonResponse(result)

    @logging_check
    def delete(self,request,email):
        """
        刪除購物車
        獲取該sku id
        獲取購物車數據
        刪除後更新redis
        回傳結果
        :param request:
        :param email:
        :return:
        """
        data = json.loads(request.body)
        id = data.get('id')
        user = request.myuser

        carts_dict = self.get_carts_dict(user.id)
        try:
            del carts_dict[id]
        except Exception as e:
            print(e)
            return JsonResponse({'code':10406,'error':'操作失敗'})
        key = f'carts_{user.id}'
        CARTS_CACHE.set(key,carts_dict)

        result = {
            'code':200,
            'data':{'carts_count':len(carts_dict)},
            'base_url':settings.PIC_URL
        }
        return JsonResponse(result)

    @logging_check
    def put(self,request,email):
        data = json.loads(request.body)
        sku_id = data.get('sku_id')
        state = data.get('state')
        print(data)

        user = request.myuser
        carts_dict = self.get_carts_dict(user.id)
        key = f'carts_{user.id}'

        # "carts_1": {"1": [3, 1], "2": [8, 0]}
        # 判斷state後修改redis數據庫
        if state == 'add':
            try:
                sku = SKU.objects.get(id=sku_id)
            except Exception as e:
                print(e)
                return JsonResponse({'code': 10407, 'error': '獲取數據失敗，請重新嘗試'})
            buy_num = carts_dict[sku_id][0] + 1
            if buy_num == sku.stock_number:
                carts_dict[sku_id][0] = buy_num
                CARTS_CACHE.set(key, carts_dict)
                return JsonResponse({'code':10408,'error':'這是最後一件了！'})
            elif buy_num > sku.stock_number:
                return JsonResponse({'code':10409,'error':'購買數量已超過庫存'})
            carts_dict[sku_id][0] = buy_num

        elif state == 'reduce':
            carts_dict[sku_id][0] -= 1
        elif state == 'select':
            carts_dict[sku_id][1] = 1
        elif state == 'unselect':
            carts_dict[sku_id][1] = 0
        elif state == 'selectall':
            for sku_id in carts_dict:
                carts_dict[sku_id][1] = 1
        elif state == 'unselectall':
            for sku_id in carts_dict:
                carts_dict[sku_id][1] = 0

        CARTS_CACHE.set(key, carts_dict)
        skus_list = self.get_skus_list(user.id)
        result = {
            'code': 200,
            'data': skus_list,
            'base_url': settings.PIC_URL
        }
        res = self.get_carts_dict(user.id)
        print(res)
        return JsonResponse(result)



    def get_carts_dict(self,user_id):
        """
        查詢購物車所有數據
        :param user_id:
        :return:
        """
        key = f'carts_{user_id}'
        carts_dict = CARTS_CACHE.get(key)
        if not carts_dict:
            return {}
        return carts_dict

    def get_skus_list(self,user_id):
        """
        獲取購物車數據的列表
        :param user_id:
        :return:
        """
        carts_dict = self.get_carts_dict(user_id)
        # print(carts_dict)
        skus_list = []
        for sku_id in carts_dict:
           sku = SKU.objects.get(id=sku_id)
           value_query = sku.sale_attr_value.all()
           sku_dict = {
               'id':sku.id,
               'image':str(sku.default_image_url),
               'name':sku.name,
               'price':sku.cost_price,
               'stock_number':sku.stock_number,
               'count':carts_dict[sku_id][0],
               'selected':carts_dict[sku_id][1],
               'sku_sale_attr_name':[i.spu_sale_attr.name for i in value_query],
               'sku_sale_attr_value':[i.name for i in value_query],
           }
           skus_list.append(sku_dict)
        # print(skus_list)
        return skus_list