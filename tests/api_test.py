import pytest
import requests


def tta_test_basic():
	resp = requests.get('http://localhost:5000/api/tta?c=1A')
	assert resp.json()['success']

def tta_test_offset():
	resp = requests.get('http://localhost:5000/api/tta?c=1A&o=-1')
	assert resp.json()['success']

def sub_test_basic():
	resp = requests.get('http://localhost:5000/api/sub?c=1A')
	assert resp.json()['success']

def sub_test_offset():
	resp = requests.get('http://localhost:5000/api/sub?c=1A&o=-1')
	assert resp.json()['success']

def cla_test():
	resp = requests.get('http://localhost:5000/api/cla')
	assert resp.json()['success']

tta_test_basic()
tta_test_offset()
sub_test_basic()
sub_test_offset()
cla_test()
