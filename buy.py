import requests
cookies = "JSESSIONID=07ed609d-3a85-4b49-9ff5-e7e482847fa4"
headers = {
    "Cookie": cookies
}
url2 ="http://202.115.122.139:8080/crossm/game/pay/event/active/667441a91d1c7c143437c60d"
data3 = {

"account": "655351028418126422",
"secondPartyAccounts": "655350830356683470"
}
response2 = requests.post(url2, headers=headers,data=data3)
print(response2.text)
