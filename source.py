import requests
cookies = "JSESSIONID=820e6495-193b-4880-81e7-2d7a0d5fea7a"
headers = {
    "Cookie": cookies
}
url2 ="http://202.115.122.139:8080/crossm/game/material/buy"
data3 = {
"id": "54b644d7eb04301fdd7c2ad7",
"urgent": "true",
"number": 10,
"money": 0
}
response2 = requests.post(url2, headers=headers,data=data3)
print(response2.text)
