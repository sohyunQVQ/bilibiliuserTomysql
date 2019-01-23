import requests
import time
import json
import mysql.connector

class Db():
    def __init__(self):
        #初始化数据库
        host = "localhost"
        user = "root"
        password = "root"
        database = "bilibili"
        self.mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.mydb.cursor()
    
    def selectData(self, mid):
        '''
        查询数据内是否有原数据
        return True: 存在
        return False: 不存在
        '''
        sql = "SELECT Id FROM users WHERE mid=%s" % mid
        self.cursor.execute(sql)
        self.cursor.fetchall()
        if self.cursor.rowcount == 0:
            return False
        else:
            return True
            
    def insertData(self, jsondata):
        '''
        插入数据
        return True: 插入成功
        return False: 插入失败
        '''
        self.__init__()
        mid = jsondata['data']['mid']
        nickname = jsondata['data']['name']
        sex = jsondata['data']['sex']
        face = jsondata['data']['face']
        sign = jsondata['data']['sign']
        level = jsondata['data']['level']
        jointime = jsondata['data']['jointime']
        birthday = jsondata['data']['birthday']
        coins = jsondata['data']['coins']
        vip = jsondata['data']['vip']['type']
        if vip == 2:
            vip = "年度大会员" 
        elif vip == 1:
            vip="大会员"
        else:
            vip="无"
        updatime = time.time()
        sql = "INSERT INTO users(`mid`, `nickname`, `sex`, `face`, `sign`, `level`, `jointime`, `birthday`, `coins`, `vip`, `updatime`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        val = (mid, nickname, sex, face, sign, int(level), jointime, birthday, coins, vip, updatime)
        self.cursor.execute(sql,val)
        self.mydb.commit()
        if self.cursor.rowcount == -1:
            return False
        else:
            printText = "插入->Id:%s, 用户名字:%s, 性别:%s, 签名:%s, 等级:%s, 注册时间:%s, 生日:%s, 硬币:%s, 会员:%s" % (mid, nickname, sex, sign, level, jointime, birthday, coins, vip)
            print(printText)
            return True

    def updateDate(self,jsondata):
        '''
        更新数据
        return True: 更新成功
        return False: 更新失败
        '''
        self.__init__()
        mid = jsondata['data']['mid']
        nickname = jsondata['data']['name']
        sex = jsondata['data']['sex']
        face = jsondata['data']['face']
        sign = jsondata['data']['sign']
        level = jsondata['data']['level']
        birthday = jsondata['data']['birthday']
        coins = jsondata['data']['coins']
        vip = jsondata['data']['vip']['type']
        if vip == 2:
            vip = "年度大会员" 
        elif vip == 1:
            vip="大会员"
        else:
            vip="无"
        updatime = time.time()
        sql = "UPDATE users SET nickname=%s, sex=%s, face=%s, sign=%s, level=%s, birthday=%s, coins=%s, vip=%s, updatime=%s WHERE mid=%s" 
        val = (nickname, sex, face, sign, int(level), birthday, coins, vip, updatime, mid)
        self.cursor.execute(sql,val)
        self.mydb.commit()
        if self.cursor.rowcount == -1:
            return False
        else:
            printText = "更新->Id:%s, 用户名字:%s, 性别:%s, 签名:%s, 等级:%s, 注册时间:%s, 生日:%s, 硬币:%s, 会员:%s" % (mid, nickname, sex, sign, level, jointime, birthday, coins, vip)
            print(printText)
            return True

def getUserinfo(mid):
    #获取用户信息
    db = Db()
    url = "http://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp" % mid
    respo = requests.get(url).text
    jsondata = json.loads(respo)
    if jsondata['code'] == 0:
        #用户存在才写入
        if db.selectData(mid):
            #更新数据
            db.updateDate(jsondata)
        else:
            #插入数据
            db.insertData(jsondata)


if __name__ == "__main__":
    i = 1
    while True:
        getUserinfo(i)
        i=i+1
        time.sleep(3)