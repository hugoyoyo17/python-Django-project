from django.core.cache import caches

from goods.models import SKU

"""
如果緩存存在數據 就從緩存中取出數據 不走視圖
如果緩存不存在的話 執行視圖函數 將視圖函數的結果保存到緩存中
"""

def cache_check(**cache_kwargs):
    def _cache_check(func):
        def wrapper(self,request,*args,**kwargs):
            if 'cache' in cache_kwargs:
                REDIS_CACHE = caches[cache_kwargs.get('cache')]
            else:
                REDIS_CACHE = caches['default']


            cache_key = cache_kwargs.get('key_prefix') + str(kwargs.get('spu_id'))
            # print(cache_key)

            res = REDIS_CACHE.get(cache_key)
            if res:
                # 如果緩存中存在數據
                print('獲取到緩存數據')
                return res
            # 如果緩存中不存在數據
            resp = func(self,request,*args,**kwargs)
            exp = cache_kwargs.get('expire',300)
            REDIS_CACHE.set(cache_key,resp,exp)
            print('從mysql獲取數據 保存到redis')
            return resp

        return wrapper
    return _cache_check