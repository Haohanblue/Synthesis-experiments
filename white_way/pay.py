import requests
import json
with open("./white_way/config.json", "r",encoding='utf-8') as f:
    cookies = json.load(f)['cookies']
# 方式一：正常付款接口
def pay_money_DIY(your_data):
    headers = {
        "Cookie": cookies
    }
    url ="http://202.115.122.139:8080/crossm/game/pay/event/active/" + your_data["pay_id"]
    data = {
            "id": your_data["pay_id"], #支付id
            "account": your_data["your_account"], #付款账户
            "secondPartyAccounts": your_data["opposite_account"], #收款账户
    }
    """
    例如:id: 6674419f1d1c7c143437c24e
        account: 655351028418126422
        secondPartyAccounts: 655350830356683470,
    """
    response = requests.post(url, headers=headers,data=data)
    return response.text

# -----------------------------------------------------------       


## 你需要修改的地方
your_data = {
    "pay_id": "66f79b38bfb79e0e90130a80", # 这里填写你的支付id
    "your_account": "655351028418126422", # 这里填写付款账户
    "opposite_account": "655351039277267475" # 这里填写收款账户
}

print(pay_money_DIY(your_data))
#print(pay_money_by_hire())
