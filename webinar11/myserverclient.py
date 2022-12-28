import requests

response = requests.get('http://127.0.0.1/')
print(response.status_code)
print(response.headers)
print(response.text[:100])

response = requests.get('http://127.0.0.1/json')
print(response.status_code)
print(response.headers)
print(response.json())
