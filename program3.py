import tkinter as tk
import tkinter.ttk as ttk

def get_score(base_price, base_score):
    for price in range(base_price, base_price + 1500):
        S_total = base_score - 10 * (price - base_price) / (0.01 * base_price)
        if S_total <= 0:
            return price - 1
    return base_price + 1500 - 1  # 如果循环完成没有低于-5的情况

class Program3Frame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        frame_left = ttk.Frame(self)
        frame_right = ttk.Frame(self)
        frame_left.grid(row=0, column=0, padx=10, pady=10)
        frame_right.grid(row=0, column=1, padx=10, pady=10)

        self.setup_frame(frame_left, 4000)
        self.setup_frame(frame_right, 6000)

    def setup_frame(self, frame, base_price):
        ttk.Label(frame, text=f"标底价格: {base_price}").grid(row=0, column=0)
        ttk.Label(frame, text="标底分数：").grid(row=1, column=0, sticky='e')
        entry_score = ttk.Entry(frame)
        entry_score.grid(row=1, column=1)
        label_price = ttk.Label(frame, text="最高价格: ")
        label_price.grid(row=2, column=0, columnspan=2)
        label_score = ttk.Label(frame, text="最低分数: ")
        label_score.grid(row=3, column=0, columnspan=2)
        button = ttk.Button(frame, text="计算最高价格",
                            command=lambda: self.calculate_and_display_max(entry_score, base_price, label_price, label_score))
        button.grid(row=4, column=0, columnspan=2)
        ttk.Label(frame, text="输入价格：").grid(row=5, column=0, sticky='e')
        entry_price = ttk.Entry(frame)
        entry_price.grid(row=5, column=1)
        label_bid_score = ttk.Label(frame, text="竞单分数: ")
        label_bid_score.grid(row=6, column=0, columnspan=2)
        button_bid = ttk.Button(frame, text="计算竞单分数",
                                command=lambda: self.calculate_bid_score(entry_price, base_price, int(entry_score.get()), label_bid_score))
        button_bid.grid(row=7, column=0, columnspan=2)

    def calculate_and_display_max(self, entry_score, base_price, label_price, label_score):
        base_score = int(entry_score.get())
        max_price = get_score(base_price, base_score)
        S_total = base_score - 10 * (max_price - base_price) / (0.01 * base_price)
        label_price.config(text=f"最高价格: {max_price}")
        label_score.config(text=f"最低分数: {S_total:.2f}")

    def calculate_bid_score(self, entry_price, base_price, base_score, label_bid_score):
        price = int(entry_price.get())
        S_total = base_score - 10 * (price - base_price) / (0.01 * base_price)
        label_bid_score.config(text=f"竞单分数: {S_total:.2f}")
