#FTP服务器
#Date:2018-12-8
#Author:Thomson


from pyftpdlib.authorizers import DummyAuthorizer,AuthenticationFailed
from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import os,sys
import logging
from hashlib import md5
from config_ftp  import *

# 添加用户权限和路径,参数分别是 用户名 密码 用户目录 权限。登录时必须输入这些添加的用户之一
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ignore_sharp(text):
    for x,item in enumerate(text):
        if item == '#':   #如果前面是#，返回空（#下标是0）
            return text[:x]
        return text             #否则继续执行

user_list=[]


#将ini文件中的账号和密码等信息存入user_list
with open("base_ftp.ini",'r') as f:
   while True:
       line = f.readline()
       # 最后一行跳出循环
       if not line:
           break
       if len(ignore_sharp(line))>3:
           user_list.append(line.split())


def add_user_to_talbe(authorizer):
   global user_list
   for user in user_list:
       name, password, permit, homedir = user
       try:
           # 添加用户
           authorizer.add_user(name, password, homedir, perm=permit)  # 具体权限看源码
       except:
           print("检查配置文件是否出错")
           print(user)

#对账号和密码进行加密
class DummyMD5Authorizer(DummyAuthorizer):
    def validate_authentication(self, username, password, handler):
          # if sys.version_info >= (3,0):
          #     password = md5(password.encode('latin1'))
          hash = md5(password.encode()).hexdigest()     #对密码进行摘要算法计算
          try:
              if self.user_table[username]['pwd'] != hash:
                  raise KeyError
          except KeyError:
              raise AuthenticationFailed



def main():
    #服务端
    # 实例化虚拟用户(所有登录FTP服务器的用户都是虚拟用户)，每当有用户请求进行验证
    authorizer = DummyMD5Authorizer()
    add_user_to_talbe(authorizer)

    # 添加匿名用户，可以不输入密码就访问
    # authorizer.add_anonymous(os.path.join(BASE_DIR,"FTPServer\\user\\ftp_user"))

    # 记录日志
    if enable_logging:
        #logging.basicConfig(filename="F:\\FTPServer\\ftp.log", level=logging.INFO)
        logging.basicConfig(filename=logging_name, level=logging.INFO)
    # 初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = authorizer

    # 被动模式
    handler.passive_ports = range(passive_ports[0],passive_ports[1])

    #设置上传下载速度,初始化限流句柄
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = max_download #下载速度
    dtp_handler.write_limit = max_upload  #上传速度

    #添加欢迎标语
    handler.banner = welcome_banner


    # 服务端
    # 监听ip 和端口 这是本地一个服务器
    address = (ip,port)
    server = FTPServer(address, handler)

    #设置最大连接数
    server.max_cons = max_conns
    server.max_cons_per_ip = max_IP

    # 开始服务
    server.serve_forever()


if __name__== '__main__':
    main()




# 日志前缀
#handler.log_prefix = '"%s"@"%s"' % (name, remote_ip)


