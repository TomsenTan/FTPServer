#密码转换程序
#Date:2018-12-8
#Author:Thomson

from hashlib import md5
import fileinput


#忽略带#号的注释行
def ignore_sharp(text):
    for x,item in enumerate(text):
        if item == '#':   #如果前面是#，返回空（#下标是0）
            return text[:x]
        return text             #否则继续执行

user_list=[]


#将ini文件中的密码修改为md5摘要模式#将ini文件中的密码修改为md5摘要模式，只需要运行一次
for line in fileinput.input('base_ftp.ini',inplace=True,mode='r',backup=''):
      if len(ignore_sharp(line))<3:
          print(line)
      else:
          user = line.split()
          user[1] = str(md5(user[1].encode()).hexdigest())  #最后将md5转换为字符串
          line_t = '   '.join(user)  #中间间隔3个空格
          print(line_t)


#打印结果，检测是否转换md5成功
with open("base_ftp.ini",'r') as f:
   while True:
       line = f.readline()
       # 最后一行跳出循环
       if not line:
           break
       if len(ignore_sharp(line))>3:
           user_list.append(line.split())



print(user_list)





