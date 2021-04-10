#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/8 16:15
# @Author    :cjw
import pytest
import json
from base.method import Requests
from common.public import file_path, write_content
from utils.file_operator import YamlOperator, ExcelOperator


class TestBook:
	excel = ExcelOperator(file_path('data', 'book.xls'), 0)
	request = Requests()

	def assert_result(self, row: int, resp):
		assert self.excel.get_except_result(row) in json.dumps(resp.json(), ensure_ascii=False)

	def test_book_001(self):
		"""获取所有书籍数据"""
		resp = self.request.get(self.excel.get_url(1))
		resp.close()
		self.assert_result(1, resp)

	def test_book_002(self):
		"""添加书籍"""
		data = self.excel.get_data(2, file_path('config', 'book.yml'))
		resp = self.request.post(self.excel.get_url(2), json=data)
		resp.close()
		book_id = resp.json()[0]['datas']['id']
		write_content(file_path('data', 'book_id'), book_id)
		self.assert_result(2, resp)

	def test_book_003(self):
		"""查看书籍"""
		resp = self.request.get(self.excel.get_url(3))
		resp.close()
		self.assert_result(3, resp)

	def test_book_004(self):
		"""更新书籍"""
		data = self.excel.get_data(4, file_path('config', 'book.yml'))
		resp = self.request.put(self.excel.get_url(4), json=data)
		resp.close()
		self.assert_result(4, resp)

	def test_book_005(self):
		"""删除书籍"""
		resp = self.request.delete(self.excel.get_url(5))
		resp.close()
		self.assert_result(5, resp)


if __name__ == '__main__':
	pytest.main(['-v', '-s', 'test_book.py'])
