import pytest
import requests

resp = requests.get('http://localhost:5000/api/sub?c=1A&o=-1')
assert resp.json()['success']
