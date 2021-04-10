#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/7 16:32
# @Author    :cjw
import requests


class Requests:
	"""接口请求，必须参数就为 method和url"""

	@staticmethod
	def request(method: str, url: str, **kwargs):
		if method.lower() == 'get':
			return requests.request('get', url, **kwargs)
		elif method.lower() == 'post':
			return requests.request('post', url, **kwargs)
		elif method.lower() == 'put':
			return requests.request('put', url, **kwargs)
		elif method.lower() == 'delete':
			return requests.request('delete', url, **kwargs)

	def get(self, url, **kwargs):
		return self.request('get', url, **kwargs)

	def post(self, url, **kwargs):
		return self.request('post', url, **kwargs)

	def put(self, url, **kwargs):
		return self.request('put', url, **kwargs)

	def delete(self, url, **kwargs):
		return self.request('delete', url, **kwargs)


if __name__ == '__main__':
	obj = Requests()
	resp = obj.get('https://www.baidu.com/')
	resp.encoding = 'utf-8'
	print(resp.text)
	resp.close()
