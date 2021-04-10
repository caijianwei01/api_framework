#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/9 11:17
# @Author    :cjw
from enum import Enum


class ApiCaseEnum(Enum):
	ID = '测试用例ID'
	MODEL = '模块'
	NAME = '接口名称'
	URL = '请求地址'
	PER = '前置条件'
	METHOD = '请求方法'
	TYPE = '请求参数类型'
	DATA = '请求参数'
	EXCEPT = '期望结果'
	IS_RUN = '是否执行'
	HEADER = '请求头'
	STATUS_CODE = '状态码'


class BookCaseEnum(Enum):
	CASE_ID = 0
	DESCRIBE = 1
	URL = 2
	METHOD = 3
	DATA = 4
	EXCEPT = 5


if __name__ == '__main__':
	print(ApiCaseEnum.ID.value)
