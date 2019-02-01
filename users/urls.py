from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path('accounts/signup/', views.signup, name='usersignup'),
    path('accounts/myaccount/', views.myaccount, name='myaccount'),
    path("", views.emailcheck, name="emailcheck"),
    path('api/signup/', views.SignupBot.as_view(), name='signup'),
    path('api/post/', views.PostBot.as_view(), name='post'),
    path('api/like/', views.LikeBot.as_view(), name='like'),
]