from django.urls import path
from django.views.decorators.cache import  cache_page
from . import views

urlpatterns = [
    path('index',cache_page(3600,cache='goods_index')(views.IndexSpiderView.as_view())),
    # path('index',views.IndexSpiderView.as_view()),
    path('',cache_page(3600,cache='lang_list')(views.ListSpiderView.as_view())),
    # path('',views.ListSpiderView.as_view()),
    path('detail/<int:lang_id>',views.DetailLangView.as_view()),
]