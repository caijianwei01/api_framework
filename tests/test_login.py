#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time      :2021/4/8 9:55
# @Author    :cjw
import pytest
from base.method import Requests
from utils.file_operator import YamlReader
from common.public import file_path

request = Requests()
yaml = YamlReader(file_path('data', 'login_test.yml'), True)


@pytest.mark.parametrize('data', yaml.data)
def test_add(data):
	resp = request.post(data['url'], json=data['body'])
	result = resp.json()
	resp.close()
	assert result['code'] == data['expect']['code']


if __name__ == '__main__':
	pytest.main(['-v', '-s', 'test_login.py'])
