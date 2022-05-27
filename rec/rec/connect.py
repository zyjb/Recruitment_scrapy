import pymysql


class Connection(object):
    def __init__(self):
        pass


    data = {    #数据库连接参数
        'host': '47.102.202.74',  #阿里云linux服务器ip地址
        'port': 3306,  #端口号
        'user': 'root', #数据库账号
        'passwd': 'chenjia', #密码
        'db': 'scrapy_django', #指定数据库
    }
    
    dbparam = dict(  #配置文件
        host=data['host'],
        port=data['port'],
        user=data['user'],
        db=data['db'],
        passwd=data['passwd'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        use_unicode=True,
    )

    def get_conn(self):
        conn = pymysql.connect(**self.dbparam)#获取一个数据库连接对象
        return conn
