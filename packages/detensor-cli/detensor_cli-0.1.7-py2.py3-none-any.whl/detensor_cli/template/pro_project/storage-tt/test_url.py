import requests

url = "http://127.0.0.1:9002/api/exec/v1/"

headers = {'Authorization':"wx-org1.chainmaker.org"}

data = {
    "uid":12,
    "orgs":["wx-org1.chainmaker.org","wx-org2.chainmaker.org"],
    "complie":True
}

response = requests.post(url, headers=headers, json=data)
print(response.text)