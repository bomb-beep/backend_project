import flask
import base64

app = flask.Flask(__name__)

plain = "1111111111"
plain_bytes = bytes(plain,"utf8")
crypt = base64.b64encode(plain)

print(crypt)