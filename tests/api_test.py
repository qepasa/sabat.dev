import pytest
import requests


def tta_test_basic():
	resp = requests.get('localhost:5000/api/tta?c=1A').json()
	assert resp['success']

def tta_test_offset():
	resp = requests.get('localhost:5000/api/tta?c=1A&o=-1').json()
	assert resp['success']

def sub_test_basic():
	resp = requests.get('localhost:5000/api/sub?c=1A').json()
	assert resp['success']

def sub_test_offset():
	resp = requests.get('localhost:5000/api/sub?c=1A&o=-1').json()
	assert resp['success']

def cla_test():
	resp = requests.get('localhost:5000/api/cla').json()
	assert resp['success']

tta_test_basic()
tta_test_offset()
sub_test_basic()
sub_test_offset()
cla_test()
