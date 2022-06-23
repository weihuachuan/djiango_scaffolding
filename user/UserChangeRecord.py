from user.models import *


class UserChangeRecord:
    @staticmethod
    def record(user_id, page_name, operation):
        """
        param: user_id 操作人工号
               page_name 当前页面名称
               operateion 当前操作
        """
        user_name = User_Data.objects.get(user_id=user_id).user_name
        User_Operate_Log.objects.create(
            user_id=user_id,
            user_name=user_name,
            current_page=page_name,
            current_operate=operation
        )
