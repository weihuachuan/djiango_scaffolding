from django.urls import path

from . import views
from user.views import *
app_name = 'user'
urlpatterns = [
    # 维护页面 维护的时候开启
    # path(r'', views.maintain, name='maintain'),
    path(r'login/', UserLoginView.as_view(), name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'user_manage/', views.user_manage, name='user_manage'),  # 用户管理主界面
    path(r'find_user_detail/', views.find_user_detail, name='find_user_detail'),  # 通过工号查询用户信息
    path(r'add_or_update_user/', views.add_or_update_user, name='add_or_update_user'),  # 新增或者修改用户信息
    path(r'delete_user/', views.delete_user, name='delete_user'),  # 删除用户信息
]