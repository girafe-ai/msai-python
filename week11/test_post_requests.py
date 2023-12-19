import requests

url = "http://localhost:8000/classify"
body = {
    "text": "I love this movie!",
    "return_proba": True,
}

response = requests.post(url, json=body)
print(response.status_code)
print(response.json())
