import requests
import json
from ast import literal_eval
url="https://northeurope.api.cognitive.microsoft.com/customvision/v3.0/Prediction/8fa281b7-7a7c-47c1-b170-676ea0d8b199/classify/iterations/carsnic/image"
headers={'content-type':'application/octet-stream','Prediction-Key':'e09004ba3d8d4cfcb6450875c3de53a8'}
r =requests.post(url,data=open("sample.png","rb"),headers=headers)
data = literal_eval(r.content.decode('utf8'))
p1 = data["predictions"][0]["probability"]
t1 = data["predictions"][0]["tagName"]
p2 = data["predictions"][1]["probability"]
t2 = data["predictions"][1]["tagName"]
print(t1, p1, t2, p2)
if (p1 > p2):
	print(t1)
else:
	print(t2)