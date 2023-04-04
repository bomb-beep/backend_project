import requests
from flask import jsonify
from json import dumps,dump,loads,load

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE+"hello/")
print(response.status_code,response.json())

response = requests.get(BASE+"posts/1/")
print(response.status_code,response.json())

response = requests.get(BASE+"posts/all/")
print(response.status_code,response.json())

data = {"post_body":"ny post",
        "Authorization":"Basic MTExMTExMTExMQ=="}
print(dumps(data))
response = requests.post(BASE+"posts/create/",json=data)
print(response.status_code, response.json())

data["post_body"] = "oppdatert post"
response = requests.put(BASE+"posts/edit/4/",json=data)
print("#")
print(response)
print(response.status_code,response.json())