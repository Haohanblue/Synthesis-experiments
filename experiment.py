import tkinter as tk
from tkinter import scrolledtext
import requests
import time
from bs4 import BeautifulSoup

def get_order_html(headers):
    url = 'http://202.115.122.139:8080/crossm/game/event?'
    response = requests.get(url, headers=headers)
    return response.text

def parse_product_completed(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    product_list = []
    rows = soup.find_all('tr', class_="success")
    for row in rows:
        first_td_text = row.find('td', class_="col-md-8").text
        if first_td_text.startswith("半自动生产线生产完成"):
            event_link = row.find('a', href=True)['href']
            event_id = event_link.split('/')[-1]
            product_list.append(event_id)
    return product_list

def parse_rent_payment(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    rent_list = []
    rows = soup.find_all('tr', class_="success")
    for row in rows:
        first_td_text = row.find('td', class_="col-md-8").text
        if first_td_text.endswith("支付租金"):
            event_link = row.find('a', href=True)['href']
            event_id = event_link.split('/')[-1]
            rent_list.append(event_id)
    return rent_list

def collect_products(headers, output):
    html_content = get_order_html(headers)
    product_ids = parse_product_completed(html_content)
    for product_id in product_ids:
        url = f"http://202.115.122.139:8080/crossm/game/line/product/event/{product_id}"
        response = requests.get(url, headers=headers)
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有类名为 'alert' 的元素
        alerts = soup.find_all(class_='alert')
        content = alerts[0].get_text()
        output.insert(tk.END, f"Requested {content}: 完成\n")
        output.see(tk.END)
        time.sleep(0.02)

def pay_all_rents(headers, output):
    html_content = get_order_html(headers)
    rent_ids = parse_rent_payment(html_content)
    i=0
    for rent_id in rent_ids:
        if i==0:
            getURL = f"http://202.115.122.139:8080/crossm/game/pay/event/{rent_id}"
            response = requests.get(getURL, headers=headers)
            # 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找支付账号的value值
            account = soup.find('select', {'name': 'account'}).find('option')['value']

            # 查找对方账号的value值
            secondPartyAccounts = soup.find('select', {'name': 'secondPartyAccounts'}).find('option')['value']
            print(account, secondPartyAccounts)
        url = f"http://202.115.122.139:8080/crossm/game/pay/event/active/{rent_id}"
        payload = {
            'id': rent_id,
            'account': account,
            'secondPartyAccounts': secondPartyAccounts
        }
        response = requests.post(url, headers=headers, data=payload)
        print(response)
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有类名为 'alert' 的元素
        alerts = soup.find_all(class_='alert')
        content = alerts[0].get_text()
        output.insert(tk.END, f"Requested {rent_id} {content} 完成\n")
        print(f"Requested {rent_id} {content} 完成\n")
        output.see(tk.END)
        time.sleep(0.02)
        i+=1

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('处理工具')
        self.geometry('600x400')

        tk.Label(self, text='输入Cookie:').pack()
        self.cookie_entry = tk.Entry(self, width=50)
        self.cookie_entry.pack()

        tk.Button(self, text='收集产品', command=self.run_collect_products).pack(pady=10)
        tk.Button(self, text='支付租金', command=self.run_pay_all_rents).pack(pady=10)

        self.output = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=10)
        self.output.pack(pady=10)

    def run_collect_products(self):
        cookie = self.cookie_entry.get()
        headers = {'Cookie': f'{cookie}'}
        headers = {k: v.strip() for k, v in headers.items()}
        collect_products(headers, self.output)

    def run_pay_all_rents(self):
        cookie = self.cookie_entry.get()
        headers = {'Cookie': f'{cookie}'}
        headers = {k: v.strip() for k, v in headers.items()}
        pay_all_rents(headers, self.output)

if __name__ == "__main__":
    app = Application()
    app.mainloop()