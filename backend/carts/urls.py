from django.urls import path
from .import views

urlpatterns = [
    path('<email>',views.CartsView.as_view()),
]