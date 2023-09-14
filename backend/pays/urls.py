from django.urls import path
from . import views

urlpatterns = [
    # path('ecpay',views.ecpay_view),
    path('return_url',views.ReturnUrlView.as_view()),
    path('orderresult_url',views.OrderResultUrlView.as_view()),
]