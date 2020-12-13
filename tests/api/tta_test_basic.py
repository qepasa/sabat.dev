import pytest
import requests

resp = requests.get('http://localhost:5000/api/tta?c=1A')
assert resp.json()['success']
