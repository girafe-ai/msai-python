import requests

response = requests.post('http://0.0.0.0:8080/tagging', json={'texts': ['God is love', 'OpenGL on the GPU is fast']})
print(response.status_code)
print(response.text)
