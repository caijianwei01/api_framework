#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/9 13:24
# @Author    :cjw
import pytest
import json
import allure
from utils.file_operator import ExcelOperator
from utils.enum import ApiCaseEnum
from common.public import file_path, write_content, read_content
from base.method import Requests

excel = ExcelOperator(file_path('data', 'api.xls'))
request = Requests()


def run_case(case: dict):
    """案例执行"""
    resp = None
    method = case[ApiCaseEnum.METHOD.value].lower()
    if method == 'get':
        if headers := case[ApiCaseEnum.HEADER.value]:
            resp = request.get(case[ApiCaseEnum.URL.value], headers=headers)
        else:
            resp = request.get(case[ApiCaseEnum.URL.value])
    elif method == 'post':
        if headers := case[ApiCaseEnum.HEADER.value]:
            if data_type := case[ApiCaseEnum.TYPE.value]:
                if data_type.lower() == 'data':
                    resp = request.post(case[ApiCaseEnum.URL.value], headers=headers, data=case[ApiCaseEnum.DATA.value])
                elif data_type.lower() == 'json':
                    resp = request.post(case[ApiCaseEnum.URL.value], headers=headers, json=case[ApiCaseEnum.DATA.value])
        else:
            if data_type := case[ApiCaseEnum.TYPE.value]:
                if data_type.lower() == 'data':
                    resp = request.post(case[ApiCaseEnum.URL.value], data=case[ApiCaseEnum.DATA.value])
                elif data_type.lower() == 'json':
                    resp = request.post(case[ApiCaseEnum.URL.value], json=case[ApiCaseEnum.DATA.value])
    elif method == 'put':
        if headers := case[ApiCaseEnum.HEADER.value]:
            if data_type := case[ApiCaseEnum.TYPE.value]:
                if data_type.lower() == 'data':
                    resp = request.put(case[ApiCaseEnum.URL.value], headers=headers, data=case[ApiCaseEnum.DATA.value])
                elif data_type.lower() == 'json':
                    resp = request.put(case[ApiCaseEnum.URL.value], headers=headers, json=case[ApiCaseEnum.DATA.value])
        else:
            if data_type := case[ApiCaseEnum.TYPE.value]:
                if data_type.lower() == 'data':
                    resp = request.put(case[ApiCaseEnum.URL.value], data=case[ApiCaseEnum.DATA.value])
                elif data_type.lower() == 'json':
                    resp = request.put(case[ApiCaseEnum.URL.value], json=case[ApiCaseEnum.DATA.value])
    elif method == 'delete':
        if headers := case[ApiCaseEnum.HEADER.value]:
            resp = request.delete(case[ApiCaseEnum.URL.value], headers=headers)
        else:
            resp = request.delete(case[ApiCaseEnum.URL.value])

    resp.close()  # 关闭连接
    return resp


def case_assert_result(resp, case: dict):
    """断言"""
    assert case[ApiCaseEnum.EXCEPT.value] in json.dumps(resp.json(), ensure_ascii=False)
    assert resp.status_code == case[ApiCaseEnum.STATUS_CODE.value]


@pytest.mark.parametrize('case', excel.run_cases)
def test_book_token(case):
    """
    1、先获取到所有前置测试点的测试用例
    2、执行前置测试点,获取结果信息
    3、拿它的结果信息替换对应测试点的变量
    4、执行当前案例
    """
    # 1、先获取到所有前置测试点的测试用例
    per_case = None
    if pre_case_id := case[ApiCaseEnum.PER.value]:
        per_case = excel.case_prev(pre_case_id)

    # 2、执行前置测试点,获取结果信息
    access_token = ''
    if per_case:
        per_resp = run_case(per_case[0])
        access_token = per_resp.json()['access_token']

    # 3、拿它的结果信息替换对应测试点的变量
    if jwt_token := case[ApiCaseEnum.HEADER.value]:
        case[ApiCaseEnum.HEADER.value]['Authorization'] = jwt_token['Authorization'].replace('{token}', access_token)

    # 4、执行当前案例
    if case[ApiCaseEnum.ID.value] in 'book_delete|book_search_one|book_update':
        book_id = read_content(file_path('data', 'book_id'))
        case[ApiCaseEnum.URL.value] = case[ApiCaseEnum.URL.value].replace('{book_id}', book_id)
    resp = run_case(case)
    if case[ApiCaseEnum.ID.value] == 'book_add':
        write_content(file_path('data', 'book_id'), resp.json()[0]['datas']['id'])
    case_assert_result(resp, case)


if __name__ == '__main__':
    pytest.main(['-v', '-s', 'test_book_token.py', '--alluredir', file_path('report', 'result')])
    import subprocess

    subprocess.call(f"allure generate {file_path('report', 'result')} -o {file_path('report', 'html')} --clean",
                    shell=True)
    subprocess.call(f"allure open -h 127.0.0.1 -p 8088 {file_path('report', 'html')}", shell=True)
