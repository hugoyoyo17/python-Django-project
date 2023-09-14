from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from .models import LangLangSpiderInfo

class IndexSpiderView(View):
    def get(self,request):
        result = self.get_lang_info()
        print(result[:4])

        return JsonResponse({'code':200,'data':result[:4]})

    def get_lang_info(self):
        """
        獲取所有浪浪資訊 並將所有data加入result中return
        filter:最後一次爬蟲時間
        :return:
        """
        info_list = LangLangSpiderInfo.objects.filter(updated_time__gt=settings.LAST_SPIDER_UPDATED_TIME)
        print('len:', len(info_list))
        # [name, gender, age, ligation, vaccination, deworming, personality, be_helped, introduction, img_url,
        # timezone.now(), timezone.now()]
        result = []
        for info in info_list:
            data = {
                'id':info.id,
                'name': info.name,
                'gender': info.gender,
                'age': info.age,
                # 'ligation':info.ligation,
                # 'vaccination':info.vaccination,
                # 'deworming':info.deworming,
                # 'personality':info.personality,
                'be_helped':info.be_helped,
                # 'introduction':info.introduction,
                'img_url':str(info.image)
            }
            result.append(data)
        return result

class ListSpiderView(View):
    def get(self,request):
        page_num = request.GET.get('page',1)
        if page_num == 'null':
            page_num = 1
        elif type(page_num) != int:
            try:
                page_num = int(page_num)
            except Exception as e:
                print(e)
                return JsonResponse({'code': 10403, 'error': '並無該分頁或分類，請重新查詢'})

        result = IndexSpiderView().get_lang_info()
        paginator = Paginator(result,15)
        try:
            page = paginator.page(page_num)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10403,'error':'並無該分頁或分類，請重新查詢'})
        data = {}
        data['objects'] = page.object_list
        data['num_pages'] = paginator.num_pages
        data['page_now'] = page_num
        print(data)
        return JsonResponse({'code': 200, 'data': data})

class DetailLangView(View):
    def get(self,request,lang_id):
        try:
            info = LangLangSpiderInfo.objects.get(id=lang_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':10413,'error':'獲取浪浪資訊失敗，請重新嘗試'})
        data = {
            'id': info.id,
            'name': info.name,
            'gender': info.gender,
            'age': info.age,
            'ligation':"是" if info.ligation else "否",
            'vaccination':info.vaccination,
            'deworming':info.deworming,
            'personality':info.personality,
            'be_helped': info.be_helped,
            'introduction':info.introduction,
            'img_url': str(info.image),
            'src':info.src
        }
        return JsonResponse({'code':200,'data':data})
