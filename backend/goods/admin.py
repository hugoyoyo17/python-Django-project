from django.contrib import admin

# Register your models here.

from .models import Catalog,Brand,SPU,SKU,SPUSaleAttr,SaleAttrValue,SKUImage,SKUComment,Stock
from django.core.cache import caches


INDEX_CACHE = caches['goods_index']
DETAIL_CACHE = caches['goods_detail']


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request,obj, form, change)
        INDEX_CACHE.clear()
        print('更新數據，刪除首頁緩存')
        spu = obj.spu
        key = f'gd{spu.id}'
        # print(key)
        DETAIL_CACHE.delete(key)
        print('更新數據，刪除詳情頁緩存')

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        INDEX_CACHE.clear()
        print('更新數據，刪除首頁緩存')
        key = f'gd{obj.id}'
        DETAIL_CACHE.delete(key)
        print('更新數據，刪除詳情頁緩存')


admin.site.register(Catalog)
admin.site.register(Brand)
admin.site.register(SPU)
# admin.site.register(SKU)
admin.site.register(SPUSaleAttr)
admin.site.register(SaleAttrValue)
admin.site.register(Stock)
admin.site.register(SKUComment)
admin.site.register(SKUImage)
