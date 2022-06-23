# djiango_scaffolding
Djaingo脚手架

## 环境说明

------

python3.8

Django==4.0.5

PyMYSQL==1.0.2

本项目包含用户登录模块和权限认证模块

## 快速启动

在项目根目录进入命令终端生成数据库表

```shell
# 生成创建数据表的命令文件
python manange.py makemigrations
# 通过命令文件创建数据库
python manage.py migrate
```

在settings.py文件中修改

```python
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',  # 数据库引擎
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'COEX_WORKSTATION',  # 你要存储数据的库名，创建的数据库mydb
        'USER': 'root',  # 数据库用户名，默认为root
        'PASSWORD': '123456',  # 密码,安装mysql时设定
        'HOST': '10.175.94.80',  # 主机
        'PORT': '7000',  # 数据库使用的端口
        'charset': 'utf8',
    }
}
```

在项目根目录进入命令终端启动项目

```python
python manage.py runserver 127.0.0.1:8080
```

## 补充知识点

### 创建Djiango项目和创建app命令

```python
# 创建Djaino项目
django-admin startproject ProjectName
# 创建App
python manange.py startapp AppName
```



