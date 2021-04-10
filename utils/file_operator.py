#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/8 9:25
# @Author    :cjw
import json
from os.path import exists
from yaml import safe_load_all, safe_load
from xlrd import open_workbook
from common.public import file_path, read_content
from utils.enum import ApiCaseEnum, BookCaseEnum


class File:

	def __init__(self, filepath: str):
		"""
		:param filepath: 文件路径
		"""
		if not exists(filepath):
			raise FileNotFoundError('文件不存在！')
		self._file_path = filepath
		self._data = None


class YamlOperator(File):

	def __init__(self, yml_path: str, multi: bool = True):
		"""
		:param yml_path: yml文件路径
		:param multi: 是否读取多个文件
		"""
		super(YamlOperator, self).__init__(yml_path)
		self._multi = multi

	@property
	def data(self):
		if not self._data:
			# 二进制读取可以不考虑编码问题
			with open(self._file_path, 'r', encoding='utf-8') as fp:
				if self._multi:
					self._data = list(safe_load_all(fp))
				else:
					self._data = safe_load(fp)
		return self._data


class ExcelOperator(File):

	def __init__(self, excel_path: str, sheet: [int, str] = 0, excel_title: bool = True):
		"""
		Excel文件读取初始化
		A  B  C
		A1 B1 C1
		A2 B2 C2

		ExcelReader(path, sheet=0).data
		[{A: A1, B: B1, C: C1},{A: A2, B: B2, C: C2}]

		ExcelReader(path, sheet=0, excel_title=False).data
		[[A1, B1, C1], [A2, B2, C2]]
		:param excel_path: excel文件路径
		:param sheet: sheet名称或者索引,默认读取索引为0的第一个Sheet
		:param excel_title: 返回数据是否带表头
		"""
		super(ExcelOperator, self).__init__(excel_path)
		self._sheet = sheet
		self._excel_title = excel_title
		self._data = []
		self._run_case = []
		self.sheet = self._get_sheet()

	@property
	def rows_num(self):
		"""获取总行数"""
		return self.sheet.nrows

	@property
	def cols_num(self):
		"""获取总列数"""
		return self.sheet.ncols

	@property
	def data(self):
		if not self._data:
			# 返回数据是否带表头
			if self._excel_title:
				title = self.sheet.row_values(0)  # 表头数据
				for row in range(1, self.sheet.nrows):
					self._data.append(dict(zip(title, self.sheet.row_values(row))))
			else:
				for row in range(1, self.sheet.nrows):
					self._data.append(self.sheet.row_values(row))
		return self._data

	@property
	def run_cases(self):
		"""获取可执行的测试用例"""
		if not self._run_case:
			for case in self.data:
				if not isinstance(case, dict):
					raise ValueError('Excel文件需要带表头读取成字典形式')
				if case.get(ApiCaseEnum.IS_RUN.value, '').lower() == 'y':
					# 状态码类型转换
					case[ApiCaseEnum.STATUS_CODE.value] = int(case[ApiCaseEnum.STATUS_CODE.value])
					# json字符串转字典
					if data := case[ApiCaseEnum.DATA.value]:
						case[ApiCaseEnum.DATA.value] = json.loads(data.strip())
					if header := case[ApiCaseEnum.HEADER.value]:
						case[ApiCaseEnum.HEADER.value] = json.loads(header.strip())
					self._run_case.append(case)
		return self._run_case

	def get_value(self, row: int, col: int):
		"""
		获取某行某列的数据
		:param row: 行数
		:param col: 列数
		:return:
		"""
		if row >= self.rows_num:
			raise ValueError(f'行数不能大于等于表格最大行数：{self.rows_num}')
		if col >= self.cols_num:
			raise ValueError(f'列数不能大于等于表格最大列数：{self.cols_num}')
		return self.sheet.cell_value(row, col)

	def get_case_id(self, row: int):
		"""获取案例id"""
		return self.get_value(row, BookCaseEnum.CASE_ID.value)

	def get_describe(self, row: int):
		"""获取案例描述"""
		return self.get_value(row, BookCaseEnum.DESCRIBE.value)

	def get_url(self, row: int):
		"""获取案例url"""
		base_url = self.get_value(row, BookCaseEnum.URL.value)
		if '{book_id}' in base_url:
			url = base_url.replace('{book_id}', read_content(file_path('data', 'book_id')))
		else:
			url = base_url
		return url

	def get_method(self, row: int):
		"""获取案例请求方法"""
		return self.get_value(row, BookCaseEnum.METHOD.value)

	def get_data(self, row: int, yml_path: str):
		"""获取案例请求的yml数据"""
		yml_list = YamlOperator(yml_path).data
		key = self.get_value(row, BookCaseEnum.DATA.value)
		# 遍历yml数据，查询key对应的数据
		data = [yt[key].get('data') for yt in yml_list if key in yt.keys()]
		return data[0] if data else None

	def get_except_result(self, row: int):
		"""获取案例请求方法"""
		return self.get_value(row, BookCaseEnum.EXCEPT.value)

	def case_prev(self, pre_condition: str):
		"""
		依据前置测试条件找到关联的前置测试用例
		:param pre_condition: 前置条件
		:return:
		"""
		case_list = []
		for case in self.run_cases:
			# 用例id等于前置条件，这个案例就是当前执行案例的前置执行案例
			if case[ApiCaseEnum.ID.value].lower() == pre_condition.lower():
				case_list.append(case)
		return case_list

	def _get_sheet(self):
		"""获取表格的sheet"""
		work_book = open_workbook(self._file_path)
		if not isinstance(self._sheet, (int, str)):
			raise TypeError(f'excel文件中sheet名字或者索引不存在：{self._sheet}')
		if isinstance(self._sheet, int):
			sheet = work_book.sheet_by_index(self._sheet)
		else:
			sheet = work_book.sheet_by_name(self._sheet)
		return sheet


if __name__ == '__main__':
	import json

	# yml_obj = YamlOperator(file_path('config', 'book.yml'))
	# print(yml_obj.data)
	# for yml in yml_obj.data:
	# 	print('book_002' in yml.keys())
	excel_obj = ExcelOperator(file_path('data', 'api.xls'))
	# for data in excel_obj.run_cases:
	# 	if case_data := data[ApiCaseEnum.DATA.value]:
	# 		print(type(case_data), case_data)
	# 	if header := data[ApiCaseEnum.HEADER.value]:
	# 		print(type(header), header)
	for data in excel_obj.run_cases:
		code = data[ApiCaseEnum.STATUS_CODE.value]
		print(type(code), code)
