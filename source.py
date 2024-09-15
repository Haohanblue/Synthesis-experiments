import requests
cookies = "JSESSIONID=07ed609d-3a85-4b49-9ff5-e7e482847fa4"
headers = {
    "Cookie": cookies
}
url2 ="http://202.115.122.139:8080/crossm/game/material/buy"
data3 = {
"id": "54b644d7eb04301fdd7c2ad7",
"urgent": "true",
"number": 3,
"money": 0
}
response2 = requests.post(url2, headers=headers,data=data3)
print(response2.text)
