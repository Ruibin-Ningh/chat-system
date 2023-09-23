#一个加密解密类
import time
import os
from cryptography.fernet import Fernet
class RBS():
    _instance = None  # 用于存储唯一的实例

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RBS, cls).__new__(cls)
            cls._instance.init_rbs()
        return cls._instance

    def init_rbs(self):
        self.timeprint('初始化RBS系统')
        # 判断如果当前目录的logs文件夹不存在，则创建
    def time(self):
        time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return f'[ {time_} ]'
    def timeprint(self,text,debug=False,timeset=True,houzhui='',fine='',n=False):#print方法
        #返回变量当前时间格式:[2018-01-01 00:00:00]使用time库
        if n == True:
            print('\n[', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']', text)
        else:
            print('[',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+']',text)
        self.log(text=text,debug=debug,file=fine,houzhui=houzhui,timeset=timeset)
    def log(self,text,debug=False,file='',houzhui='',timeset=True):#日志文件
        if not os.path.exists('./logs/'):
            os.mkdir('./logs/')
        # 保存日志追加内容文件命名格式年月日时分秒毫秒
        # 不存在则创建文件格式年月日时分秒毫秒
        text = str(text)
        text = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']' + text +'\n'
        file1 = './logs/' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.log'
        if debug:
            if timeset:
                file1 = file + time.strftime('%Y%m%d', time.localtime(time.time())) + houzhui
            else:
                file1 = file + houzhui
        if not os.path.exists(file1):
            self.save(text,file1 ,2,)
        else:
            self.save(text,file1,1,)
    def save(self,text,file,pattern,help=False):#text保存文本,file是保存目录,pattern选择保存模式[3种模式:1是追加,2是覆盖,3是二进制模式,如果都不是则直接使用参数,如:直接输入'a'则是追加等]注意二进制是覆盖模式
        text = str(text)
        #如果目录保存文件不存在则创建
        if help == True:
            self.timeprint('你触发了帮助机制:text保存文本,file是保存目录,pattern选择保存模式[3种模式:1是追加,2是覆盖,3是二进制模式,如果都不是则直接使用参数,如:直接输入 a 则是追加等]注意二进制是覆盖模式')
            self.log('RBS:用户触发save方法的help机制')
        if pattern == 1:
            with open(file, 'a') as f:
                f.write(text)
                f.close()
        elif pattern == 2:
            with open(file, 'w') as f:
                f.write(text)
                f.close()
        elif pattern == 3:
            with open(file, 'wb') as f:
                f.write(text)
                f.close()
        else:
            with open(file, pattern) as f:
                f.write(text)
                f.close()
    def encryption(self,text,key=b'KR9X3GsB3e-S93U_aR6sBRC9EzpXj5b0zhs_DNwzYrw=',save=(False,'./encipher.rbs')):
        self.log('RBS:用户触发加密方法')
        key = Fernet(key)
        data_to_encrypt = key.encrypt(text.encode('utf-8'))
        if save[0] == False:
            return data_to_encrypt
        else:
            self.save(data_to_encrypt,save[1],2)
    def decryption(self,text,key=b'KR9X3GsB3e-S93U_aR6sBRC9EzpXj5b0zhs_DNwzYrw=',save=(False,'./decipher.rbs')):
        self.log('RBS:用户触发解密方法')
        key = Fernet(key)
        data_to_decrypt = key.decrypt(text)
        if save[0] == False:
            return data_to_decrypt
        else:
            self.save(data_to_decrypt,save[1],2)
    def read(self,file):
        self.log('RBS:用户触发读取方法')
        with open(file, 'r') as f:
            data = f.read()
            f.close()
        return eval(data)
