import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import time

class Program1Frame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.parent, text='输入Cookie:').pack()
        self.cookie_entry = ttk.Entry(self.parent, width=50)
        self.cookie_entry.pack()

        self.output = scrolledtext.ScrolledText(self.parent, wrap=tk.WORD, width=70, height=10)
        self.output.pack(pady=10)

        ttk.Button(self.parent, text='收集产品', command=self.run_collect_products).pack(pady=10)
        ttk.Button(self.parent, text='支付租金', command=self.run_pay_all_rents).pack(pady=10)

    def run_collect_products(self):
        cookie = self.cookie_entry.get()
        headers = {'Cookie': f'{cookie}'}
        headers = {k: v.strip() for k, v in headers.items()}
        self.collect_products(headers)

    def run_pay_all_rents(self):
        cookie = self.cookie_entry.get()
        headers = {'Cookie': f'{cookie}'}
        headers = {k: v.strip() for k, v in headers.items()}
        self.pay_all_rents(headers)

    def collect_products(self, headers):
        html_content = self.get_order_html(headers)
        product_ids = self.parse_product_completed(html_content)
        for product_id in product_ids:
            url = f"http://202.115.122.139:8080/crossm/game/line/product/event/{product_id}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            alerts = soup.find_all(class_='alert')
            content = alerts[0].get_text() if alerts else response.text
            self.output.insert(tk.END, f"Requested {content}: 完成\n")
            self.output.see(tk.END)
            time.sleep(0.02)

    def pay_all_rents(self, headers):
        html_content = self.get_order_html(headers)
        rent_ids = self.parse_rent_payment(html_content)
        for rent_id in rent_ids:
            url = f"http://202.115.122.139:8080/crossm/game/pay/event/active/{rent_id}"
            response = requests.post(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            alerts = soup.find_all(class_='alert')
            content = alerts[0].get_text() if alerts else response.text
            self.output.insert(tk.END, f"Requested {rent_id} {content} 完成\n")
            self.output.see(tk.END)
            time.sleep(0.02)

    def get_order_html(self, headers):
        url = 'http://202.115.122.139:8080/crossm/game/event?'
        response = requests.get(url, headers=headers)
        return response.text

    def parse_product_completed(self, html_content):
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

    def parse_rent_payment(self, html_content):
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