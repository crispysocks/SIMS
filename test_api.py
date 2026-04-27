import urllib.request
import json

def test_endpoint(url, headers=None):
    print(f"\nTesting: {url}")
    req = urllib.request.Request(url, method='GET')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        resp = urllib.request.urlopen(req)
        print(f"  Status: {resp.status}")
        print(f"  Body: {resp.read().decode()[:100]}")
    except urllib.error.HTTPError as e:
        print(f"  Status: {e.code}")
        print(f"  Body: {e.read().decode()}")
    except Exception as e:
        print(f"  Error: {e}")

headers = {'X-User': 'admin', 'X-Roles': 'admin'}

# Test with headers
test_endpoint('http://127.0.0.1:8000/teachers', headers)
test_endpoint('http://127.0.0.1:8000/classes', headers)

# Test without headers
test_endpoint('http://127.0.0.1:8000/teachers')
test_endpoint('http://127.0.0.1:8000/classes')
