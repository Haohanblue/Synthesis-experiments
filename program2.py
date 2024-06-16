import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup

class Program2Frame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.cities = [
            {"id": "54c78c101bf42f56b14a91ee", "name": "成都", "L": "", "H": "", "HURL": "", "LURL": "", "power": ""},
            {"id": "54c78e5c1bf42f56b14a93cb", "name": "亚洲", "L": "", "H": "", "HURL": "", "LURL": "", "power": ""},
            {"id": "54bdea47eb048d9802ef3e89", "name": "武汉", "L": "", "H": "", "HURL": "", "LURL": "", "power": ""},
            {"id": "54acef16eb04d4137be47d8c", "name": "北京", "L": "", "H": "", "HURL": "", "LURL": "", "power": ""},
            {"id": "54c78cb91bf42f56b14a9203", "name": "深圳", "L": "", "H": "", "HURL": "", "LURL": "", "power": ""},
            {"id": "54c78ce91bf42f56b14a920b", "name": "大连", "L": "", "H": "", "HURL": "", "LURL": "", "power": ""},
            {"id": "54c78c771bf42f56b14a91f5", "name": "沈阳", "L": "", "H": "", "HURL": "", "LURL": "", "power": ""}
        ]
        self.auto_update_id = None
        self.countdown = 5
        self.entries = {}
        self.cities_dict = {city['id']: city for city in self.cities}
        self.create_widgets()

    def print_to_gui(self, message):
        self.output_text.configure(state='normal')
        self.output_text.insert('end', message + '\n')
        self.output_text.configure(state='disabled')
        self.output_text.yview('end')

    def fetch_power_data(self):
        for city in self.cities:
            city_id = city['id']
            url = f"http://202.115.122.139:8080/crossm/game/area/gen/mine/{city_id}"
            cookie_value = self.cookie_entry.get()
            headers = {
                'Cookie': cookie_value.strip(),
            }
            response = requests.post(url,headers=headers)
            if response.status_code == 200:
                try:
                    data = response.json().get('data', [])
                    my_company = next((item for item in data if item['name'] == "我的企业"), None)
                    other_companies = next((item for item in data if item['name'] == "其他企业"), None)
                    if my_company and other_companies:
                        my_value = my_company['value']
                        other_value = other_companies['value']
                        if other_value != 0:
                            power_percentage = (my_value / (my_value + other_value)) * 100
                            city['power'] = f"{power_percentage:.2f}%"
                        else:
                            city['power'] = "100.00%"
                    else:
                        city['power'] = "N/A"
                except ValueError:
                    self.print_to_gui(f"JSON解析错误: {response.text}")
                    city['power'] = "Error"
            else:
                self.print_to_gui(f"请求失败: {response.status_code}")
                city['power'] = "Error"
            self.tree.item(city['id'], values=(city['name'], city['H'], city['L'], city['power']))

    def submit_data(self):
        for city_id, (h_entry, l_entry) in self.entries.items():
            h_value = h_entry.get()
            l_value = l_entry.get()
            base_url = "http://202.115.122.139:8080/crossm/game/order/require/"
            cookie_value = self.cookie_entry.get()
            headers = {
                'Cookie': cookie_value.strip(),
            }
            if h_value:
                h_url = base_url + self.cities_dict[city_id]['HURL']
                response = requests.post(h_url, data={'number': h_value}, headers=headers, allow_redirects=False)
                if response.status_code == 302:
                    response_message = f"城市：{self.cities_dict[city_id]['name']}，H型产品数量：{h_value}，URL：{h_url}\n响应状态码：{response.status_code}, 响应内容：订单提交成功"
                    self.print_to_gui(response_message)
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    alerts = soup.find_all(class_='alert')
                    content = alerts[0].get_text() if alerts else response.text
                    response_message = f"城市：{self.cities_dict[city_id]['name']}，H型产品数量：{h_value}，URL：{h_url}\n响应状态码：{response.status_code}, 响应内容：{content}"
                    self.print_to_gui(response_message)
            if l_value:
                l_url = base_url + self.cities_dict[city_id]['LURL']
                response = requests.post(l_url, data={'number': l_value}, headers=headers, allow_redirects=False)
                if response.status_code == 302:
                    response_message = f"城市：{self.cities_dict[city_id]['name']}，L型产品数量：{l_value}，URL：{l_url}\n响应状态码：{response.status_code}, 响应内容：订单提交成功"
                    self.print_to_gui(response_message)
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    alerts = soup.find_all(class_='alert')
                    content = alerts[0].get_text() if alerts else response.text
                    response_message = f"城市：{self.cities_dict[city_id]['name']}，L型产品数量：{l_value}，URL：{l_url}\n响应状态码：{response.status_code}, 响应内容：{content}"
                    self.print_to_gui(response_message)
        self.update_data()

    def manage_timer(self, start=False):
        if self.auto_update_id:
            self.master.after_cancel(self.auto_update_id)
        if start:
            self.auto_update_id = self.master.after(5000, self.update_data)
        self.countdown_label.config(text=f"下次更新还有 {self.countdown} 秒")
        self.countdown = 5
        self.master.after(1000, self.countdown_timer)

    def countdown_timer(self):
        if self.countdown > 0:
            self.countdown -= 1
            self.countdown_label.config(text=f"下次更新还有 {self.countdown} 秒")
            self.master.after(1000, self.countdown_timer)

    def update_data(self):
        total_L = 0
        total_H = 0
        cookie_value = self.cookie_entry.get()
        headers = {"Cookie": cookie_value.strip()}
        for city in self.cities:
            url = f"http://202.115.122.139:8080/crossm/game/order/require/{city['id']}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            panel_headings = soup.find_all('div', class_="panel-heading")
            for div in panel_headings:
                if 'L型 订单信息' in div.get_text():
                    l_remain_span = div.find('span', string=lambda text: '剩余数量' in text)
                    if l_remain_span:
                        city['L'] = l_remain_span.text.split(':')[1].strip()
                        total_L += int(city['L'])

                if 'H型 订单信息' in div.get_text():
                    h_remain_span = div.find('span', string=lambda text: '剩余数量' in text)
                    if h_remain_span:
                        city['H'] = h_remain_span.text.split(':')[1].strip()
                        total_H += int(city['H'])

            self.tree.item(city['id'], values=(city['name'], city['H'], city['L'], city['power']))
            sales_divs = soup.find_all('div', attrs={'data-title': 'H型产品销售数据统计'})
            if sales_divs:
                city['HURL'] = sales_divs[0].get('id', '')[4:]

            sales_divs = soup.find_all('div', attrs={'data-title': 'L型产品销售数据统计'})
            if sales_divs:
                city['LURL'] = sales_divs[0].get('id', '')[4:]

            self.tree.item(city['id'], values=(city['name'], city['H'], city['L'], city['power']))
        self.tree.item('total', values=("合计", total_H, total_L))
        self.fetch_power_data()  # Fetch power data after updating
        self.manage_timer(start=True)

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(side='left', fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=('City', 'H', 'L', 'Power'), show='headings')
        self.tree.heading('City', text='城市', anchor='center')
        self.tree.heading('H', text='H型', anchor='center')
        self.tree.heading('L', text='L型', anchor='center')
        self.tree.heading('Power', text='影响力', anchor='center')
        self.tree.column('City', anchor='center')
        self.tree.column('H', anchor='center')
        self.tree.column('L', anchor='center')
        self.tree.column('Power', anchor='center')
        self.tree.pack(side='left', fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(side='left', fill='both', expand=True)

        header_frame = ttk.Frame(self.input_frame, padding=5)
        header_frame.pack(fill='x', expand=True)
        ttk.Label(header_frame, text="H型").pack(side='left', padx=50)
        ttk.Label(header_frame, text="L型").pack(side='left', padx=30)

        for city in self.cities:
            city_frame = ttk.Frame(self.input_frame, padding=5)
            city_frame.pack(fill='x', expand=True)
            ttk.Label(city_frame, text=f"{city['name']}").pack(side='left')
            h_entry = ttk.Entry(city_frame, width=10)
            h_entry.pack(side='left', padx=5)
            l_entry = ttk.Entry(city_frame, width=10)
            l_entry.pack(side='left', padx=5)
            self.entries[city['id']] = (h_entry, l_entry)

        for city in self.cities:
            entry_h = ttk.Entry(self.master, width=5)
            entry_l = ttk.Entry(self.master, width=5)
            self.tree.insert('', 'end', iid=city['id'], values=(city['name'], city['L'], city['H'], city['power']))
        self.tree.insert('', 'end', iid='total', values=("合计", "", "", ""))

        self.cookie_label = ttk.Label(self.master, text="请输入Cookie:")
        self.cookie_label.pack()
        self.cookie_entry = ttk.Entry(self.master)
        self.cookie_entry.pack()

        self.update_button = ttk.Button(self.master, text="更新数据", command=self.update_data)
        self.update_button.pack()

        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(fill='x', expand=False)
        self.submit_button = ttk.Button(self.button_frame, text="提交订单", command=self.submit_data)
        self.submit_button.pack(pady=10)

        self.countdown_label = ttk.Label(self.master, text=f"下次更新还有 {self.countdown} 秒")
        self.countdown_label.pack()

        self.output_frame = ttk.Frame(self.master)
        self.output_frame.pack(fill='x', expand=True)
        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=20, state='disabled')
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)

        self.manage_timer(start=True)

if __name__ == "__main__":
    root = tk.Tk()
    Program2Frame(root).pack(fill="both", expand=True)
    root.mainloop()
