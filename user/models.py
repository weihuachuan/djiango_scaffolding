from django.db import models


# Create your models here.
class User_Data(models.Model):
    # id
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    user_id = models.CharField(max_length=800, null=True, verbose_name='用户id')
    user_password = models.CharField(max_length=1200, null=True, verbose_name='用户密碼')
    user_name = models.CharField(max_length=800, null=True, verbose_name='用户姓名')
    user_permission = models.CharField(max_length=800, null=True, verbose_name='用户权限')
    user_extension = models.CharField(max_length=800, null=True, verbose_name='用户分机')
    operator_id = models.CharField(max_length=800, null=True, verbose_name='操作人工号')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    objects = models.Manager()

    class Meta:
        db_table = 'user_data'
        verbose_name = '用户管理'

    def __str__(self):
        return self.user_id


class User_Operate_Log(models.Model):
    # id
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    user_id = models.CharField(max_length=800, null=True, verbose_name='用户id')
    user_name = models.CharField(max_length=800, null=True, verbose_name='用户姓名')
    current_page = models.CharField(max_length=800, null=True, verbose_name='當前頁面')
    current_operate = models.CharField(max_length=800, null=True, verbose_name='當前操作')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    modify_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')
    objects = models.Manager()

    class Meta:
        db_table = 'user_operate_log'
        verbose_name = '用户操作記錄表'

    def __str__(self):
        return self.user_id
