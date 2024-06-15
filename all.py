import tkinter as tk
from tkinter import ttk
from program3 import Program3Frame  # 引入程序3模块
from program2 import Program2Frame
from program1 import Program1Frame
class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('综合实验处理脚本')
        self.geometry('900x600')

        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        self.program1_tab = ttk.Frame(self.tab_control)
        self.program2_tab = ttk.Frame(self.tab_control)
        self.program3_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.program1_tab, text='处理事件')
        self.tab_control.add(self.program2_tab, text='市场销售')
        self.tab_control.add(self.program3_tab, text='价格计算')

        self.init_program1()
        self.init_program2()
        self.init_program3()

    def init_program1(self):
        program1_frame = Program1Frame(self.program1_tab)
        program1_frame.pack(fill=tk.BOTH, expand=True)

    def init_program2(self):
        program2_frame = Program2Frame(self.program2_tab)
        program2_frame.pack(fill=tk.BOTH, expand=True)

    def init_program3(self):
        program3_frame = Program3Frame(self.program3_tab)
        program3_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
