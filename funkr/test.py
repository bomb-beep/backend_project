import requests
from requests import get,post,put,delete
from flask import jsonify
from json import dumps,dump,loads,load
from base64 import b64encode

def test(method,request,args = {}):
	if request[-1] != "/":
		request = request + "/"
	print(f"--{request}--")
	response = method("http://127.0.0.1:5000/"+request,json=args)
	print(f"Status code: {response.status_code}")
	print(f"Content-type: {response.headers['Content-type']}")
	if response.headers["Content-type"] == "application/json":
		print(f"{response.json()}\n")
	else:
		print(f"{response.content}\n")

def check(request,expected_response=None):
	if request[-1] != "/":
		request = request + "/"
	print(f"check {request}")
	response = get("http://127.0.0.1:5000/"+request)
	if expected_response is not None:
		print(f"Expected response: {expected_response},  actual response: {response}")
	if response.content is None:
		print(f"{response.status_code}")
	elif response.headers["Content-type"] == "application/json":
		print(f"Status code: {response.status_code}\n{response.json()}\n\n")
	else:
		print(f"Status code: {response.status_code}\n{response.content}\n\n")

def authorization_token(key):
	return "Basic "+str(b64encode(bytes(key,"utf8")),"utf8")


#print(authorization_token("1111111111"))
print("Initialize test database")
test(post,"testdb")

print("Test 'hello'")
test(get,"hello")
#check("hello","Hello!")
print("Test get individual post")
test(get,"posts/1")
print("Test get all posts")
test(get,"posts/all")

data = {"post_body":"ny post",
	"Authorization":authorization_token("1111111111")}
print("Test create post: 'ny post'")
test(post,"posts/create",data)
check("posts/4")
check("posts/all")

data["post_body"] = "oppdatert post"
print("Update 'ny post' 'oppdatert post'")
test(put,"posts/edit/4",data)
check("posts/4")

data["Authorization"] = authorization_token("2222222222")
print("Test unauthorized update 'Innlegg nummer en'")
test(put,"posts/edit/1",data)
check("posts/1")

print("Test delete post 'oppdatert post'")
test(post,"posts/delete/4",{"Authorization":authorization_token("1111111111")})
check("posts/4")

print("Test unauthorized delete 'Innlegg nummer en'")
test(post,"posts/delete/1",{"Authorization":authorization_token("2222222222")})
check("posts/1")