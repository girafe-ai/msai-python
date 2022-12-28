import requests

# Example of GET request with additional headers specified

response = requests.get(
    'https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages',
    headers={'My': 'Value'},
)
print(response)
print(type(response))
print(dir(response))

print('-' * 100)

print(response.status_code)
print(response.headers)
print(response.text[:100])


# Example of POST request with JSON in response's body

print('-' * 100)

response = requests.post('https://httpbin.org/post')
print(response)
print(response.text)
print(response.json())
