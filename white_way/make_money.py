import requests
import json
with open("./white_way/config.json", "r",encoding='utf-8') as f:
    cookies = json.load(f)['cookies']

#方式一：扩建厂房挣钱
def make_money_by_plus_factory(your_data):
    headers = {
        "Cookie": cookies
    }
    url ="http://202.115.122.139:8080/crossm/game/factory/plus"
    data = {
            "id": your_data["id"],
            "area": your_data["area"],
            "money": your_data["money"],
    }
    response = requests.post(url, headers=headers,data=data)
    return response.text




# -----------------------------------------------------------   
# 你需要修改的地方
your_data = {
    "id": "6653d42c1d1c7c1434319756", # 这里填写你的厂区id
    "area": 0,           # 这里填写你要扩建的厂房面积,厂区最大面积为4316
    "money": -20000000,  # 这里填写你要投入的资金，正为支出，负为收入
}
print(make_money_by_plus_factory(your_data))
