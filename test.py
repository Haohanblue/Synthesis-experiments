import requests

cookies = "JSESSIONID=07ed609d-3a85-4b49-9ff5-e7e482847fa4"
headers = {
    "Cookie": cookies
}
data = {
    "pid": "665d323b1d1c7c14340adb00",
"number": 2
}
# data2 = {
#     "id": "667428fb1d1c7c1434332146",
#     "account": "655351028418126422",
#     "secondPartyAccounts": "655350830356683470"
# }
url = "http://202.115.122.139:8080/crossm/game/order/require/contract/666fabce1d1c7c14342522776"
response = requests.post(url, headers=headers)
print(response.text)

# url2 ="http://202.115.122.139:8080/crossm/game/line/receivepro/665d33ea1d1c7c14340ccc5e"
# data3 = {
#     "bomid": "54c84a071bf4bbf787013514",
#     "number": 20000
# }
# response2 = requests.post(url2, headers=headers, data=data3)
# print(response2.text)