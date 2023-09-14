from django.urls import path
from .import views
from django.views.decorators.cache import  cache_page

urlpatterns = [
    # path('index',views.GoodsIndexView.as_view()),
    path('index',cache_page(3600,cache='goods_index')(views.GoodsIndexView.as_view())),
    path('detail/<int:spu_id>',views.GoodsDetailView.as_view()),
    path('sku',views.GoodsDetailView.as_view()),
    path('catalogs/',views.GoodsListView.as_view()),
]