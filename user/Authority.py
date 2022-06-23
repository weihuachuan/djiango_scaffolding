from user.Jwt import Jwt
from .models import User_Data

# 白名单
white_list = ['F1237077']


class Authority:
    @staticmethod
    def get_auth(token):
        """
        获取当前登录操作者的工号和权限等级
        return user_id 工号 auth 权限登记
        """
        user_auth_dic = {"op": 1, "engineer": 2, "dri": 3, "manager": 4, "superuser": 5}
        result = Jwt.decode(token, "1234567")
        # 当前用户
        user_id = result['user_id']
        auth = user_auth_dic[result['authority']]
        return user_id, auth

    @staticmethod
    def get_update_user_auth(user_id):
        """
        通过工号获取用户权限等级
        """
        user_auth_dic = {"op": 1, "engineer": 2, "dri": 3, "manager": 4, "superuser": 5}
        user = User_Data.objects.get(user_id=user_id)
        auth = user_auth_dic[user.user_permission]
        return auth

    @staticmethod
    def get_white_list():
        """
        获取白名单列表
        """
        return white_list
