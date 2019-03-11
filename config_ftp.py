#配置选项
#Date:2018-12-8
#Author:Thomson

ip = "0.0.0.0"
#ip = "127.0.0.1"  #只能本机用于测试，若希望局域网内用户可访问，设置为0.0.0.0
port = 10000


#对上下传文件速度作一定限流
#上传速度  200Kb/s
max_upload = 20 * 1024
#下载速度  40Kb/s
max_download = 40 * 1024

#最大连接数，根据实际需求更改
#最大连接数(并发数)
max_conns = 200
#最多IP连接数
max_IP = 10

#被动连接端口,注意：端口数必须比客户端连接数多否则客户端不能连接
passive_ports = (2000, 2500)

#是否允许匿名访问
enable_anonymous = False

#是否打开日志记录，默认情况是False
enable_logging = True

#日志记录文件名称,会在当前文件夹内生成ftp.lgo文件。必须是要用r原生的字符串
logging_name = r"ftp.log"

#欢迎标语
welcome_banner = r"欢迎来到 XXX FTP站点"

