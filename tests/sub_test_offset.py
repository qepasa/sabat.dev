import pytest
import requests

def test():
	resp = requests.get('http://localhost:5000/api/sub?c=1A&o=-1')
	print(resp.json())
	assert resp.json()['success']

test()