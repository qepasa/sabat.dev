import pytest
import requests

resp = requests.get('http://localhost:5000/api/cla')
assert resp.json()['success']
