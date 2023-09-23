import socket
import subprocess
import struct
import threading
from threading import Thread
import save

stop = False
def prints(txt):
    pr=save.RBS()
    pr.timeprint(text=txt,debug=True,timeset=True,houzhui='.log',fine='./logs/server',n=False)
class S():
    def __init__(self,host='192.168.0.137',port=1145):
        self.user = {}#用户信息
        self.Safety_list = []#安全名单
        self.sms(host,port)
    def sms(self,host='192.168.0.137',port=1145):
        self.HOST = host
        self.PORT = port
        self.ADDR = (host, port)

        prints(f'[+] 服务器地址:{self.HOST}:{self.PORT}')
        self.BUFFSIZE = 2048 #接收缓冲区大小
        MAX_LISTEN = 10 #最大连接设备数量
        prints(f'[+] 服务器接收缓冲大小:{self.BUFFSIZE}\n                       [+] 服务器最大设备连接数{MAX_LISTEN}')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(self.ADDR)
            server.listen(MAX_LISTEN)
            while True:
                conn, addr = server.accept()
                self.user[addr] = conn
                save.RBS().timeprint(text=f'[+] IP{addr} 尝试连接服务器',debug=True,timeset=True,houzhui='.log',fine='./logs/server',n=True)

                # 使用新线程处理客户端连接
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()

    def handle_client(self, conn, addr):
        try:
            # 添加一个字典用于跟踪用户发送的消息及其重复次数
            message_count = {}

            while True:
                data = conn.recv(self.BUFFSIZE)
                data = data.decode('utf-8')
                if not data:
                    pass

                # 检查消息是否已经达到15次重复
                if data in message_count:
                    message_count[data] += 1
                    if message_count[data] > 15:
                        prints(f'[-] 用户{addr}发送的消息"{data}"超过15次重复，将被剔除')
                        break
                else:
                    message_count[data] = 1

                # 处理消息（您的现有逻辑）
                self.Chat(data, addr, conn)
                prints(f'[+] 用户{addr}向服务器发送数据：{data}')
                self.Secure_encryption(data, addr, conn)
        except Exception as e:
            # 处理异常
            prints(f'[-] 用户{addr}断开连接，原因:{e}，自动删除其名单\n')

            del self.user[addr]
            if addr in self.Safety_list:
                self.Safety_list.remove(addr)

            for key, value in self.user.items():
                if value != conn:
                    self.users(value)
                    value.send(f'//用户 {addr} 下线了，期间不会受到短信'.encode())
            prints(f'[+] [Chat] 已给所有用户发送用户{addr}下线提示')
        finally:
            conn.close()
    def Chat(self,data,addr,conn):#聊天系统
        if data[0:2] == '@/':
            user = ''
            chat = ''
            type = False
            for i in data[2::]:#通过遍历来获得用户名与聊天消息
                if type == True:
                    chat += i
                elif i == '/':
                    type = True
                else:
                    user += i
            user = eval(user)
            prints(f'用户{addr}向{user}发送短信:{chat}')
            conn.send(f'//您已向{user}发送短信:{chat}'.encode())
            self.user[user].send(f'@/{user}/{chat}'.encode())


    def Secure_encryption(self,data,addr,conn):#安全加密方法
        if addr in self.Safety_list:
            return None
        prints(f'[+] [密] 向用户{addr}发送安全加密')
        if data == '/Ruibin/':
            prints(f'[+] [密] 用户{addr}通过安全加密')
            conn.send('&/Ruibin'.encode('utf-8'))
            prints(f'[+] [密] 用户{addr}发送服务器内部信息')
            self.users(conn)
            conn.send('//欢迎加入Ruibin运营商'.encode('utf-8'))
            conn.send(f'//请记住你的IP与端口,他相当你的id,您的IP{addr}'.encode('utf-8'))
            self.Safety_list.append(addr)#将用户加入安全名单
            prints(f'[+] [密] 用户{addr}加入安全名单')
            for key,value in self.user.items():#遍历所有用户告诉他们新用户上线
                if value != conn:
                    self.users(value)
                    value.send(f'//用户 {addr} 上线'.encode())
            prints(f'[+] [Chat] 以给所有用户{addr}发送用户上线提示')
        else:
            conn.close()
            prints(f'[-] [密] 用户{addr}未通过安全加密')

    def Return_data(self,addr,txt,conn,):#发送消息方法
        conn.send(txt.encode('utf-8'))
        prints((f'[+] 向用户{addr}发送数据:{txt}'))
    def users(self,conn):
        user = []
        for key,value in self.user.items():
            if  value == conn:
                user.append('您')
            else:
                user.append(key)
        conn.send(f'@!{user}'.encode('utf-8'))

#本机ip
prints(f'本机IP:{socket.gethostbyname(socket.gethostname())}')
S(host=input('IP:'),port=1145)