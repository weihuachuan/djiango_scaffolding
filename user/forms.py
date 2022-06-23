#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：NewSams 
@File ：forms.py.py
@Author ：吾非同
@Date ：2022/4/6 下午 05:02 
"""
from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={
        'required': '账号必须填写',
    })
    password = forms.CharField(required=True, min_length=3, max_length=100, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少3位',
        'max_length': '密码不能超过100位'
    })
