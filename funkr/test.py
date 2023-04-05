import requests
from requests import get,post,put,delete
from flask import jsonify
from json import dumps,dump,loads,load

def test(method,request,args = {}):
	if request[-1] != "/":
		request = request + "/"
	print(f"--{request}--")
	response = method("http://127.0.0.1:5000/"+request,json=args)
	print(f"Status code: {response.status_code}")
	print(f"Content-type: {response.headers['Content-type']}")
	print(f"{response.json()}\n")

def check(request):
	if request[-1] != "/":
		request = request + "/"
	print(f"check {request}")
	response = get("http://127.0.0.1:5000/"+request)
	if response.content is None:
		print(f"{response.status_code}")
	else:
		print(f"{response.status_code} {response.json()}\n\n")

test(post,"testdb")

test(get,"hello")
test(get,"posts/1")
test(get,"posts/all")

data = {"post_body":"ny post",
	"Authorization":"Basic MTExMTExMTExMQ=="}
test(post,"posts/create",data)
check("posts/4")

data["post_body"] = "oppdatert post"
test(put,"posts/edit/4",data)
check("posts/4")

test(post,"posts/delete/4",{"Authorization":"Basic MTExMTExMTExMQ=="})
check("posts/4")