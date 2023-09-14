import hashlib

from django.core.cache import caches
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from carts.views import CartsView
from orders.models import *

from .sample_create_order_ALL import main

import importlib.util
import urllib.parse

from django.conf import settings

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    "pays/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

CARTS_CACHE = caches['carts']

# Create your views here.

def ecpay_view(request):
    return HttpResponse(main())


class ReturnUrlView(View):
    """
    確認checkmacvalue 如正確回傳1|OK
    """
    def post(self,request):
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID=settings.ECPAY_MERCHANTID,
            HashKey=settings.ECPAY_HASHKEY,
            HashIV=settings.ECPAY_HASHIV
        )
        HashKey = 'pwFHCqoQZGmho4w6'
        HashIV = 'EkRm7iFT261dpevs'
        res = request.POST.dict()
        print('res',res)
        back_check_mac_value = res.get('CheckMacValue')
        res.pop('CheckMacValue')
        # result = []
        # for k,v in res.items():
        #     query = f'{k}={v}'
        #     result.append(query)
        #
        # query_string = '&'.join(result)
        # print('query_string',query_string)
        # hash_query = f'Hashkey={HashKey}&{query_string}&HashIV={HashIV}'
        # print(hash_query)
        # encode_url = urllib.parse.quote(hash_query).lower()
        # print('encode_url',encode_url)
        # my_check_mac_value = hashlib.sha256(encode_url.encode('utf-8')).hexdigest().upper()
        # print(my_check_mac_value)
        # print(back_check_mac_value)

        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value:
            print(1)
            return HttpResponse('1|OK')
        print(0)
        return HttpResponse('0|Fail')

class OrderResultUrlView(View):
    """
    確認付款結果 如check_mac_value正確 Rtncode==1 RtnMsg==succeeded 回到商店付款成功頁面
    失敗導向失敗頁面
    """
    def post(self,request):
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID=settings.ECPAY_MERCHANTID,
            HashKey=settings.ECPAY_HASHKEY,
            HashIV=settings.ECPAY_HASHIV
        )
        res = request.POST.dict()
        print('res', res)
        back_check_mac_value = res.get('CheckMacValue')
        res.pop('CheckMacValue')

        RtnCode = res.get('RtnCode')
        RtnMsg = res.get('RtnMsg')
        order_id = res.get('MerchantTradeNo')
        settlement_type = res.get('CustomField1').split('=')[1]
        order = OrderInfo.objects.get(order_id=order_id)

        check_mac_value = ecpay_payment_sdk.generate_check_value(res)
        if check_mac_value == back_check_mac_value and RtnCode=='1' and RtnMsg=='Succeeded':
            # print(1)
            order_goods_list = OrderGoods.objects.filter(order_info=order)
            for goods in order_goods_list:
                sku = goods.sku
                # 已經在訂單建立時暫時扣除****
                # sku.stock_number -= goods.count
                # sku.sales += goods.count
                # sku.save()

            user = order.user_profile
            carts_dict = CartsView().get_carts_dict(user.id)
            # 扣除購物車中數量並返回
            if settlement_type == '0':
                carts_dict_0 = {k: v for k, v in carts_dict.items() if v[1] == 0}
                key = f'carts_{user.id}'
                CARTS_CACHE.set(key,carts_dict_0)
                print(carts_dict_0)
                carts_count = len(carts_dict_0)

            else:
                carts_count = len(carts_dict)
            order.status = 2
            order.save()
            pay_success_url = f'http://localhost:7001/miumiushop/site/pay_success.html?carts_count={carts_count}'
            return HttpResponseRedirect(pay_success_url)
        order.status=0
        order.save()
        pay_failed_url = f'http://localhost:7001/miumiushop/site/pay_failed.html'
        return HttpResponseRedirect(pay_failed_url)
