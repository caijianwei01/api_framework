#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/8 9:17
# @Author    :cjw
import os

base_path = os.path.dirname(os.path.dirname(__file__))


def file_path(file_dir: str, filename: str):
	"""
	获取文件路径
	:param file_dir: 目录
	:param filename: 文件名称
	:return:
	"""
	return os.path.join(base_path, file_dir, filename)


def write_content(path: str, content):
	"""
	:param path:
	:param content:
	:return:
	"""
	with open(path, 'w', encoding='utf-8') as f:
		f.write(str(content))


def read_content(path: str):
	"""
	:param path:
	:param content:
	:return:
	"""
	with open(path, 'r', encoding='utf-8') as f:
		content = f.read()
	return content


if __name__ == '__main__':
	# print(file_path('data', 'login_test.yml'))
	rs = read_content(file_path('data', 'book_id'))
	print(type(rs), rs)
