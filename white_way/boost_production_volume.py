import requests
import json
with open("./white_way/config.json", "r",encoding='utf-8') as f:
    cookies = json.load(f)['cookies']
# 方式一：投产
def boost_production_volume(your_data):
    headers = {
        "Cookie": cookies
    }
    url ="http://202.115.122.139:8080/crossm/game/line/receivepro/" + your_data["line_id"]
    data = {
      "number": your_data["number"],
    }
    response = requests.post(url, headers=headers,data=data)
    return response.text
your_data = {
    "line_id":"665d308c1d1c7c1434081310", # 这里填写你的产线id
    "number": 500000, # 这里填写你要投产的数量
}

print(boost_production_volume(your_data))