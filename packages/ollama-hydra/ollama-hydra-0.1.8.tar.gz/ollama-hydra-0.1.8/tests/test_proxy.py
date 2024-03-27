# tests/test_proxy.py
import requests

def test_proxy_status_code():
    response = requests.get('http://localhost:11434')  # Assuming your proxy is running
    assert response.status_code == 200
