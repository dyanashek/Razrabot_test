import requests
import pprint

# response = requests.get('http://127.0.0.1:5000/tasks')
# response = requests.get('http://127.0.0.1:5000/task/1')
# response = requests.post('http://127.0.0.1:5000/tasks', json={'title': 'you', 'description': 'descr2',})
response = requests.delete('http://127.0.0.1:5000/task/6')
# response = requests.put('http://127.0.0.1:5000/task/1', json={'title': 'test_changed'})
pprint.pprint(response.json())
pprint.pprint(response.status_code)

