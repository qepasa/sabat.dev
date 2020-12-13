import pytest
import requests

def test():
	resp = requests.get('http://localhost:5000/api/cla')
	assert resp.json()['success']

test()
