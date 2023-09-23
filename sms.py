import socket
import tkinter as tk
from tkinter import scrolledtext
import threading
import save

userm = {}

class sms:
    def __init__(self):
        pass

    def prints(self, txt):
        pr = save.RBS()
        pr.timeprint(text=txt, debug=True, timeset=True, houzhui='.log', fine='./logs/sms')
        self.send(txt)

    def send(self, txt):
        self.chat_display.config(state="normal",font='黑体')  # 设置为可编辑
        self.chat_display.insert(tk.END, f"\n{save.RBS().time()} {txt}  \n")
        self.chat_display.config(state="disabled",font='黑体')  # 设置为只读
        # 清空消息输入框
        self.message_entry.delete(0, tk.END)

    def panduan(self, data, server):
        if data[0:2] == '//':
            self.prints(f'[官方] [{server}运营商] 短信消息:{data[2::]}')
            return False

        if data[0:2] == '@/':

            user = ''
            chat = ''
            type = False
            for i in data[2::]:  # 通过遍历来获得用户名与聊天消息
                if type == True:
                    chat += i
                elif i == '/':
                    type = True
                else:
                    user += i

            user = eval(user)  # 将字符串转化元祖
            self.prints(f'[{user}] [{server}运营商] 向您发起短信消息:{chat}')  # 输出
        elif data[0:2] == "@!":
            userm =data[2::]
            self.user = userm
            self.prints(f'[+] 用户信息获取成功,在线用户:{self.user}')

    def windows(self):
        self.root = tk.Tk()
        self.root.title("运营商")
        self.root.resizable(False, False)  # 防止用户更改窗口大小
        self.app = self
        self.server = False

        # 创建聊天显示窗口，设置为只读
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=120, height=40,
                                                      state="disabled",font='黑体')
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        # 创建消息输入框，设置为可编辑
        self.message_entry = tk.Entry(self.root, width=100,font='黑体')
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        # 创建发送按钮
        self.send_button = tk.Button(self.root, text="发送",font='黑体',command=lambda:self.send_(self.message_entry.get()))
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.root.mainloop()
    def send_(self,txt):
        self.s.send(bytes(str(txt), encoding='utf-8'))
        self.prints(f'[+] 向服务端发送成功:{txt}')
    def run(self, ip, p):
        HOST = ip
        PORT = p
        ADDR = (HOST, PORT)
        ENCODING = 'utf-8'
        BUFFSIZE = 2048
        def run():
            Rz = False
            with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as self.s:
                self.s.connect(ADDR)
                server = ''
                self.prints(f'[+] 发现附近服务端,尝试进入\n                       [+]服务端IP:{HOST}:{PORT}')
                while True:
                    if Rz == False:
                        self.s.send(b'/Ruibin/')
                    data = self.s.recv(BUFFSIZE).decode(ENCODING)
                    if data:
                        print(data)
                    if Rz == False:
                        if data[0] == '&' and data[1] == '/':
                            Rz = True
                            server = data[2::]
                            continue
                    if self.panduan(data, server):
                        self.prints(f'[{server}运营商] 短信消息:{data}')
                    else:
                        continue

        t1 = threading.Thread(target=self.windows)
        t2 = threading.Thread(target=run)

        t1.start()
        t2.start()

if __name__ == '__main__':
    ip = input('IP:')
    port = input('PORT:')
    susapp = sms()
    susapp.run(ip, int(port))
