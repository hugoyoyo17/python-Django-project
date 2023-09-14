import json
import time

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from utils.logging_dec import logging_check
from goods.models import SKU
from users.models import Address
from carts.views import CartsView
from django.core.cache import caches
from .models import OrderInfo,OrderGoods
from pays.views import main


CARTS_CACHE = caches['carts']
PAYS_CACHE = caches['pays_check']

class AdvanceView(View):
    @logging_check
    def get(self,request):
        user = request.myuser
        """
        1.點擊購物車中去結算settlement_type=0
        2.點擊商品詳情中立即購買spu=1&settlement_type=1
        """
        settlement_type = request.GET.get('settlement_type')
        print(settlement_type)

        if settlement_type == '0':
            skus_list = CartsView().get_skus_list(user.id)
            # print(skus_list)
            order_result = []
            for sku in skus_list:
                if sku.get('selected') == 1:
                    order_result.append(sku)
            # print(order_result)

            # 獲取送貨地址
            addr_list = self.get_address(user)
            # print(addr_list)
            result = {
                'code':200,
                'data':{'address':addr_list,'skus_list':order_result},
                'base_url':settings.PIC_URL
            }
            print(result)
            return JsonResponse(result)

        # 直接購買從網址獲取spu_id 購買銷售屬性值 及數量
        elif settlement_type == '1':
            spu_id = request.GET.get('spu_id')
            sale_attr_value = request.GET.get('sale_attr_value')
            count = request.GET.get('count')
            if not sale_attr_value or not spu_id or not count:
                return JsonResponse({'code':10407,'error':'請求數據有誤'})
            sku = SKU.objects.get(spu=spu_id,sale_attr_value=sale_attr_value,is_launched=True)
            value_query = sku.sale_attr_value.all()
            addr_list = self.get_address(user)
            sku_list = []
            sku_dict = {
                'id':sku.id,
                'name':sku.name,
                'image':str(sku.default_image_url),
                'price':sku.cost_price,
                'count':count,
                'selected':1,
                'sku_sale_attr_name':[i.spu_sale_attr.name for i in value_query],
                'sku_sale_attr_value':[i.name for i in value_query]
            }
            sku_list.append(sku_dict)
            result = {
                'code':200,
                'data':{'address':addr_list,'skus_list':sku_list},
                'base_url':settings.PIC_URL
            }
            print(result)
            return JsonResponse(result)




    def get_address(self,user):
        """
        獲取個人地址資訊(如果有填寫)
        :param user:
        :return:
        """
        address_list = Address.objects.filter(user_profile=user)
        result = []
        for address in address_list:
            addr = address.address.split('-')
            county = addr[0]
            district = addr[1]
            road = addr[2]
            # print(county,district,road)
            dict = {
                'id':address.id,
                'receiver':address.receiver,
                'receiver_phone':address.receiver_phone,
                'county':county,
                'district':district,
                'road':road
            }
            result.append(dict)
        return result


class OrderView(View):
    @logging_check
    def post(self,request,email):
        """
        1.建立訂單
        2.添加訂單商品
        3.減少庫存 判定庫存是否足夠(暫時)*****
        4.返回響應
        :param request:
        :param email:
        :return:
        """
        data = json.loads(request.body)
        settlement_type = data.get('settlement_type')
        pay_method = data.get('pay_method')
        freight = data.get('freight')
        remark = data.get('remark')
        addr_id = data.get('addr_id')

        spu_id = data.get('spu_id')
        count = data.get('count')
        sale_attr_value = data.get('sale_attr_value')
        print('data:',data)

        user = request.myuser


        if settlement_type not in [0,1]:
            return JsonResponse({"code": 10404, "error": '數據有誤'})

        try:
            address = Address.objects.get(id=addr_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10407,'error':'請求數據有誤'})

        order_id = f'{time.strftime("%Y%m%d%H%M%S")}{user.id}'
        total_amount = 0
        total_count = 0

        order = OrderInfo.objects.create(
            user_profile = user,
            order_id = order_id,
            total_amount = total_amount,
            total_count = total_count,
            pay_method = pay_method,
            freight = freight,
            status = 1,
            receiver = address.receiver,
            receiver_phone = address.receiver_phone,
            address = address.address,
            remark = remark
        )

        # carts_dict = {1:[2,1],2:[8,0]}
        carts_dict = CartsView().get_carts_dict(user.id)
        # 從購物車中購買的 確認是否還有庫存** 並更新銷量與庫存
        if settlement_type == 0:
            for k,v in carts_dict.items():
                # selected = 1 選中購買的
                if v[1] == 1:
                    sku = SKU.objects.filter(id=k,is_launched=True)
                    if not sku:
                        return JsonResponse({'code':10410,'error':'商品已下架'})
                    sku = sku[0]
                    # print(sku)
                    count = v[0]
                    if count>sku.stock_number:
                        return JsonResponse({'code':10411,'error':f'{sku.name}庫存不足僅剩{sku.stock_number}件'})
                    sku.stock_number -= count
                    sku.sales += count
                    sku.save()

                    order_goods = OrderGoods.objects.create(
                        order_info = order,
                        sku = sku,
                        count = count,
                        price = sku.cost_price
                    )
                    total_count += order_goods.count
                    total_amount += order_goods.price* order_goods.count

            order.total_count = total_count
            order.total_amount = total_amount
            order.save()
        # 直接購買
        else:
            sku = SKU.objects.filter(spu=spu_id,sale_attr_value=sale_attr_value,is_launched=True)
            if not sku:
                return JsonResponse({'code': 10410, 'error': '商品已下架'})
            sku = sku[0]
            count = int(count)
            if count>sku.stock_number:
                return JsonResponse({'code': 10411, 'error': f'{sku.name}庫存不足僅剩{sku.stock_number}件'})
            sku.stock_number -= count
            sku.sales += count
            sku.save()

            order_goods = OrderGoods.objects.create(
                order_info=order,
                sku=sku,
                count=count,
                price=sku.cost_price
            )
            total_count += count
            total_amount += order_goods.price * count

            order.total_count = total_count
            order.total_amount = total_amount
            order.save()

        # 購物車購買的話 更新購物車：只保留未勾選之商品(v[1]==0)(更改至結帳完成後)****
        # 獲取生成Ecpay訂單所需之data
        if settlement_type == 0:
            # carts_dict_0 = {k:v for k,v in carts_dict.items() if v[1]==0}
            # key = f'carts_{user.id}'
            # CARTS_CACHE.set(key,carts_dict_0)
            # carts_count = len(carts_dict_0)
            order_goods_all = OrderGoods.objects.filter(order_info=order)
            item_name = '#'.join([goods.sku.name + ' ' + str(int(goods.sku.cost_price)) + ' 元' + ' x ' + str(goods.count) for goods in order_goods_all])


        else:
            # carts_count = len(carts_dict)
            item_name = order_goods.sku.name + ' ' + str(int(order_goods.sku.cost_price)) + ' 元' + ' x ' + str(order_goods.count)
        data = {
            'trade_no':order.order_id,
            'total_amount':int(total_amount)+int(order.freight),
            'item_name':item_name,
            'remark':order.remark,
            'settlement_type':settlement_type
        }

        # 建立訂單後 存入redis倒數 若超過繳款時間 將訂單狀態修改為0
        key = f'pays_{user.id}_{order.order_id}'
        PAYS_CACHE.set(key,data)


        return JsonResponse({'code':200,'data':main(**data)})

class GetOrderInfoView(View):
    @logging_check
    def get(self,request):
        user = request.myuser
        orders = OrderInfo.objects.filter(user_profile=user).order_by('-order_id')
        result = []
        for order in orders:
            # 如果訂單狀態是待繳費 從redis中獲取key是否存在
            # 存在:附上綠界繳費網址
            # 不存在:判定為過期 交易取消
            if order.status == 1:
                key = f'pays_{user.id}_{order.order_id}'
                dict_data = PAYS_CACHE.get(key)
                if dict_data:
                    data = {
                        'order_id': order.order_id,
                        'order_time': str(order.created_time).split('.')[0],
                        'total_amount': int(order.total_amount + order.freight),
                        'status': order.status,
                        'pay_url':main(**dict_data)
                    }
                    result.append(data)
                    continue
                else:
                    order.status = 0
                    order.save()
            data = {
                'order_id':order.order_id,
                'order_time':str(order.created_time).split('.')[0],
                'total_amount':int(order.total_amount+order.freight),
                'status':order.status
            }
            result.append(data)
        print(result)
        return JsonResponse({'code':200,'data':result})
    @logging_check
    def put(self,request):
        """
        如用戶按確認收件 更改訂單狀態為已完成
        :param request:
        :return:
        """
        data = json.loads(request.body)
        print(data)
        order_id = data.get('order_id')
        try:
            order = OrderInfo.objects.get(order_id=order_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10401,'error':'系統異常'})

        order.status = 4
        order.save()

        return JsonResponse({'code':200,'data':{'order_status':order.status}})


class GetOrderDetailView(View):
    @logging_check
    def get(self,request,order_id):
        """
        獲取訂單詳細資訊
        :param request:
        :param order_id:
        :return:
        """
        try:
            order = OrderInfo.objects.get(order_id=order_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10412,'error':'查無此訂單'})

        order_goods = OrderGoods.objects.filter(order_info=order)
        skus_list = []
        for goods in order_goods:
            value_query = goods.sku.sale_attr_value.all()
            dict = {
                'id':goods.sku.id,
                'spu_id':goods.sku.spu.id,
                'name':goods.sku.name,
                'image':str(goods.sku.default_image_url),
                'price':goods.sku.cost_price,
                'count':goods.count,
                'sku_sale_attr_name':[i.spu_sale_attr.name for i in value_query],
                'sku_sale_attr_value':[i.name for i in value_query]
            }
            skus_list.append(dict)
        print(skus_list)

        return JsonResponse({'code':200,'data':{'skus_list':skus_list,'freight':order.freight,'order_id':order_id},'base_url':settings.PIC_URL})

class PutCartsAgainView(View):
    @logging_check
    def post(self,request,email):
        """
        用戶如欲回購 按取重新加入購物車選項 將該訂單所購買之商品再次加入購物車
        :param request:
        :param email:
        :return:
        """
        data = json.loads(request.body)
        order_id = data.get('order_id')
        user = request.myuser

        order = OrderInfo.objects.get(order_id=order_id)
        order_goods = OrderGoods.objects.filter(order_info=order)
        carts_dict = CartsView().get_carts_dict(user.id)
        # print(carts_dict)
        for goods in order_goods:
            sku_id = goods.sku.id
            count = goods.count
            if sku_id in carts_dict.keys():
                if count>goods.sku.stock_number:
                    return JsonResponse({'code': 10411, 'error': f'{goods.sku.name}庫存不足僅剩{goods.sku.stock_number}件'})
                carts_dict[sku_id][0]+=count
            else:
                carts_dict[sku_id] = [count,1]
        print(carts_dict)
        key = f'carts_{user.id}'
        CARTS_CACHE.set(key,carts_dict)



        return JsonResponse({'code':200,'carts_count':len(carts_dict)})







