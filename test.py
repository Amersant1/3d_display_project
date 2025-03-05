import requests


request = requests.post("http://localhost:8000/create_client", json={"name": "123"})
print(request.text)
