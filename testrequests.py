import requests

r = requests.get('http://127.0.0.1:5000/api/users/1',
                 headers={'content-type': 'application/json'})
print(r.json())