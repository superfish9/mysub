#encoding=utf-8
import MySQLdb
import time

#日志记录
def log(tag, message):
    f = open('/tmp/mysub/db.log', 'a+')
    f.write('[%s] %s: %s\n' % (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), tag, message))
    f.close()
    return

class Mysql(object):
    def __init__(self, host='127.0.0.1', port=3306, user='', passwd='', name=''):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.name = name
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.name)
        self.cur = self.conn.cursor()
    
    def insert(self, table='', columns=(), values=()):
        sql = 'insert into ' + table + str(columns).replace("'", "") + ' ' + str(values) + ';'
        try:
            self.cur.execute(sql)
            log('insert', '%s [success]' % sql)
            return True
        except:
            log('insert', '%s [fail]' % sql)
            return False
    
    def delete(self, table='', where=''):
        sql = 'delete from ' + table + ' where ' + where + ';'
        try:
            self.cur.execute(sql)
            log('delete', '%s [success]' % sql)
            return True
        except:
            log('delete', '%s [fail]' % sql)
            return False
    
    def update(self, table='', dset='', where=''):
        sql = 'update ' + table + ' set ' + dset + ' where ' + where + ';'
        try:
            self.cur.execute(sql)
            log('update', '%s [success]' % sql)
            return True
        except:
            log('update', '%s [fail]' % sql)
            return False        
    
    def select(self, columns=(), table='', where=''):
        sql = 'select ' + str(columns).replace("'", "").replace("(", "").replace(")", "") + ' from ' + table + ' where ' + where +';'
        try:
            self.cur.execute(sql)
            log('select', '%s [success]' % sql)
            return self.cur.fetchall()
        except:
            log('select', '%s [fail]' % sql)
            return False
    
    def __del__(self):
        self.cur.close()
        self.conn.close()
        