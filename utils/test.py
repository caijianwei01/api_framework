#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/9 14:23
# @Author    :cjw

if __name__ == '__main__':
	headers = {'Authorization': 'JWT {token}'}
	print('{token}' in headers)
	for k, v in headers.items():
		if '{token}' in v:
			headers[k] = v.replace('{token}', '123')
	print(headers)
