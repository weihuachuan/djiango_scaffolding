import json
import logging
from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.Authority import Authority
from user.Jwt import Jwt
from user.UserChangeRecord import UserChangeRecord
from user.forms import UserLoginForm
from user.models import User_Data
logger = logging.getLogger(__name__)
user_auth_dic = {"op": 1, "engineer": 2, "dri": 3, "manager": 4, "superuser": 5}


def check_cookie_user_id(fun):
    """
    装饰器函数，用于检查当前用户的登陆状态
    """

    def check(*args, **kwargs):
        try:
            token = args[0].COOKIES.get('token', '')
        except AttributeError:
            token = args[1].COOKIES.get('token', '')
        result = Jwt.decode(token, "1234567")
        if result['user_id'] == ' ':
            # context = {'msg': '用户登陆已经过期，请重新登陆'}
            return redirect(reverse('user:login'))
        res = fun(*args, **kwargs)
        return res

    return check


class UserLoginView(View):
    @staticmethod
    def get(request):
        """显示登录页面"""
        # 判断是否记住了用户名
        log_year = datetime.today().year
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            password = request.COOKIES.get('password')
            checked = 'checked'
        else:
            username, password, checked = '', '', ''
        return render(request, 'login.html', {
            'username': username, 'checked': checked, 'password': password, 'log_year': log_year
        })

    @csrf_exempt
    def post(self, request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            user_id = user_login_form.cleaned_data['username']
            user_password = user_login_form.cleaned_data['password']
            context = {"status": 0, "msg": ''}
            obj = User_Data.objects.filter(user_id=user_id, user_password=user_password, is_delete=False).first()
            if obj:
                context['status'] = 1
                token = Jwt.encode({"user_id": user_id, "user_name": obj.user_name, "authority": obj.user_permission},
                                   "1234567", 12 * 3600)  # 制作令牌
                # 默认跳转到首页
                next_url = request.GET.get('next', reverse('user:user_manage'))
                # 跳转到next_url
                ret = redirect(next_url)
                ret.set_cookie('token', token, 12 * 3600)
                return ret
            else:
                context['msg'] = '账号或密码错误，请重新输入'
                return render(request, "login.html", context)
        else:
            return render(request, 'login.html', {
                'user_login_form': user_login_form
            })


@check_cookie_user_id
def logout(request):
    response = HttpResponseRedirect('/user/login/')
    response.delete_cookie('token')
    return response


@check_cookie_user_id
def user_manage(request):
    """
    param keyword
    返回用户管理界面所有用户的数据
    return context
    """
    context = {}
    # 获取前端传过来的keyword
    keyword = request.GET.get('keyword', '')
    user_data = User_Data.objects.filter(is_delete__exact=False)
    # 获取页面用户信息头数据
    comment_data = get_user_page_head(request)
    if keyword == '':
        context['user_data'] = user_data
        context['keyword'] = keyword
    else:
        user_data_filter = user_data.filter(Q(user_id__contains=keyword) | Q(user_name__contains=keyword) |
                                            Q(user_permission__contains=keyword) | Q(user_extension__contains=keyword))
        context['user_data'] = user_data_filter
        context['keyword'] = keyword
    context['comment_data'] = comment_data
    return render(request, 'user_manage.html', context)


def get_user_page_head(request):
    token = request.COOKIES.get('token', '')
    result = Jwt.decode(token, "1234567")
    result['datetime'] = datetime.now().strftime("%Y-%m-%d")
    # 将权限名称分级
    result['authority'] = user_auth_dic[result['authority']]
    return result


@csrf_exempt
def find_user_detail(request):
    """
    param： user_id
    获取用户的个人信息
    reusrn context dict
    """
    context = {'status': 0, 'msg': "查询失败", 'data': {}}
    if request.method == "POST":
        user_id = request.POST.get('user_id', '')
        if user_id == '':
            return context
        else:
            user_dict = get_user_data(user_id)
            context['data'] = user_dict
            context['status'] = 1
            context['msg'] = ""
            return JsonResponse(context)


def get_user_data(user_id):
    """
    通过user_id 从数据库查数据返回
    return user_dict
    """
    user_dict = {}
    try:
        user = User_Data.objects.get(user_id=user_id)
        user_dict["user_name"] = user.user_name
        user_dict["user_id"] = user.user_id
        user_dict["password"] = user.user_password
        user_dict["permission"] = user.user_permission
        user_dict["phone"] = user.user_extension
    except Exception as e:
        logger.error(e)
    return user_dict


@csrf_exempt
def add_or_update_user(request):
    """
    param： user_data
    修改或者新增用户
    return context dict
    """
    context = {'status': 0, 'msg': "操作失敗"}
    if request.method == "POST":
        try:
            # 获取当前用户的token
            token = request.COOKIES.get('token', '')
            # 获取当前用户的工号和权限等级
            operator_id, operator_auth = Authority.get_auth(token)
            # 获取前端操作标识
            flag = request.POST.get('flag')
            # 获取前端要跟新用户的数据
            user_data = json.loads(request.POST.get('data'))
            # todo 判空
            context = is_blank(user_data)
            if context['status'] == 0:
                return JsonResponse(context)
            if flag == 'update':
                context = update_user(user_data, operator_id, operator_auth)
            elif flag == 'add':
                context = add_user(user_data, operator_id, operator_auth)
        except Exception as e:
            logger.error(e)
        return JsonResponse(context)


def update_user(user_data, operator_id, operator_auth):
    user_id = user_data['user_id']
    try:
        # todo 校验
        user_auth = Authority.get_update_user_auth(user_id)
        # 要赋予的权限
        to_auth = user_auth_dic[user_data['authority']]
        flag = is_authority(operator_auth, user_id, user_auth, to_auth)
        if flag:
            user = User_Data.objects.get(user_id=user_data['user_id'])
            user.user_id = user_data['user_id']
            user.user_name = user_data['user_name']
            user.user_permission = user_data['authority']
            user.user_extension = user_data['phone']
            user.user_password = user_data['password']
            user.save()
            UserChangeRecord.record(operator_id, "用户管理界面", "修改%s成功" % user_id)
            context = {'status': 1, 'msg': "修改人員成功"}
        else:
            UserChangeRecord.record(operator_id, "用户管理界面", "修改%s失败" % user_id)
            context = {'status': 0, 'msg': "無權限修改"}
    except Exception as e:
        UserChangeRecord.record(operator_id, "用户管理界面", "修改%s失败" % user_id)
        logger.error(e)
        context = {'status': 0, 'msg': "修改人員失敗"}
    return context


def add_user(user_data, operator_id, operator_auth):
    context = {'status': 0, 'msg': "新增人員失敗"}
    user_id = user_data['user_id']
    user_auth = user_auth_dic[user_data['authority']]
    try:
        # todo 权限校验
        flag = is_authority(operator_auth, user_id, user_auth)
        if flag:
            # 判断要创建的人是否存在
            user = User_Data.objects.filter(user_id=user_data['user_id']).first()
            if user:
                if user.is_delete is True:
                    user.is_delete = False
                    user.user_id = user_data['user_id']
                    user.user_name = user_data['user_name']
                    user.user_permission = user_data['authority']
                    user.user_extension = user_data['phone']
                    user.user_password = user_data['password']
                    user.save()
                    UserChangeRecord.record(operator_id, "用户管理界面", "新增%s成功" % user_id)
                    context = {'status': 1, 'msg': "新增人員成功"}
                else:
                    context['msg'] = "用户已经存在"
            else:
                User_Data.objects.create(
                    user_id=user_data['user_id'],
                    user_name=user_data['user_name'],
                    user_permission=user_data['authority'],
                    user_extension=user_data['phone'],
                    user_password=user_data['password'],
                    operator_id=operator_id
                )
                UserChangeRecord.record(operator_id, "用户管理界面", "新增%s成功" % user_id)
                context = {'status': 1, 'msg': "新增人員成功"}
        else:
            UserChangeRecord.record(operator_id, "用户管理界面", "新增%s失败" % user_id)
            context = {'status': 0, 'msg': "無權限新增"}
    except Exception as e:
        UserChangeRecord.record(operator_id, "用户管理界面", "新增%s失败" % user_id)
        logger.error(e)
        context = {'status': 0, 'msg': "新增人員失敗"}
    return context


@csrf_exempt
def delete_user(request):
    """
    param： user_id
    删除用户 (假删除 其数据会在数据库中保存)
    return context dict
    """
    context = {'status': 0, 'msg': "刪除人員失敗"}
    if request.method == "POST":
        try:
            # 获取当前用户的token
            token = request.COOKIES.get('token', '')
            # 获取当前用户的工号和权限等级
            operator_id, operator_auth = Authority.get_auth(token)
            # 获取要删除人的工号
            user_id = request.POST.get('user_id')
            context = del_user(user_id, operator_id, operator_auth)
        except Exception as e:
            logger.error(e)
        return JsonResponse(context)


def del_user(user_id, operator_id, operator_auth):
    """
    删除用户数据库操作
    param: user_id被删除人工号 operator_id 操作人工号 operator_auth 操作人权限
    return: dict 状态码 和 信息
    """
    try:
        # todo 权限校验
        user_auth = Authority.get_update_user_auth(user_id)
        # 要赋予的权限 这里无意义
        # to_auth = Authority.get_update_user_auth(user_id)
        flag = is_authority(operator_auth, user_id, user_auth)
        if flag:
            # 删除用户 标记删除
            user = User_Data.objects.get(user_id=user_id)
            user.is_delete = True
            user.operator_id = operator_id
            user.save()
            UserChangeRecord.record(operator_id, "用户管理界面", '删除%s成功' % user_id)
            context = {'status': 1, 'msg': "刪除人員成功"}
        else:
            UserChangeRecord.record(operator_id, "用户管理界面", '删除%s失败' % user_id)
            context = {'status': 0, 'msg': "無權限刪除"}
    except Exception as e:
        UserChangeRecord.record(operator_id, "用户管理界面", '删除%s失败' % user_id)
        logger.error(e)
        context = {'status': 0, 'msg': "刪除人員失敗"}
    return context


def is_authority(operator_auth, user_id, user_auth, to_auth=0):
    """
    判断操作人是否有权限操作被操作人
    param: operator_auth, user_auth,user_id  操作者权限、被操作者权限、被操作人id
    return boolean
    """
    if user_id in Authority.get_white_list():
        return False
    if operator_auth == 5:
        return True
    elif operator_auth == 3 or operator_auth == 4:
        if operator_auth > user_auth and operator_auth > to_auth:
            return True
        else:
            return False
    else:
        return False


def is_blank(user_data):
    context = {'status': 1, 'msg': ""}
    if user_data['user_name'] == '':
        context['status'] = 0
        context['msg'] = '姓名不能為空！'
        return context
    if user_data['user_id'] == '':
        context['status'] = 0
        context['msg'] = '工號不能為空！'
        return context
    if user_data['authority'] is None or user_data['authority'] == '':
        context['status'] = 0
        context['msg'] = '權限不能為空！'
        return context
    if user_data['password'] == '':
        context['status'] = 0
        context['msg'] = '密碼不能為空！'
        return context
    return context


def edit_token(request, auth):
    # 获取token信息
    token = request.COOKIES.get('token', '')
    result = Jwt.decode(token, "1234567")
    token = Jwt.encode({"user_id": result['user_id'], "user_name": result['user_name'], "authority": auth},
                       "1234567", 12 * 3600)  # 制作令牌
    return token

