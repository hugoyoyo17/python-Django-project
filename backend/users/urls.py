from django.urls import path
from .import views

urlpatterns= [
    path('',views.UserViews.as_view()),
    path('activation',views.active_view),
    path('<email>/check_active',views.check_active_view),
    path('password/get_verify',views.forget_password_getverify_view),
    path('password/check_verify',views.check_verify_view),
    path('password/newpass',views.update_password_view),
    path('<email>/change_pass',views.ChangePassword.as_view()),
    path('google/user',views.GoogleOauthToken.as_view()),
    path('fb/user',views.FbOauthToken.as_view()),
    path('<email>/address',views.Personal_info_View.as_view()),
    path('<email>/verify',views.info_get_verify_view),
]