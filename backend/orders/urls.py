from django.urls import path
from . import views




urlpatterns = [
    path('advance',views.AdvanceView.as_view()),
    path('<email>',views.OrderView.as_view()),
    path('',views.GetOrderInfoView.as_view()),
    path('order_detail/<int:order_id>',views.GetOrderDetailView.as_view()),
    path('<email>/carts',views.PutCartsAgainView.as_view()),
]