#encoding=utf-8
import sys
import json
import base64
import time
from http import do_get, do_post
from db import Mysql

sys.path.append('..')
import config.config as conf

#日志记录
def log(tag, message):
    f = open('/tmp/mysub/sqlimanage.log', 'a+')
    f.write('[%s] %s: %s\n' % (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), tag, message))
    f.close()
    return

#sql注入管理类
class SqliManage(object):
    def __init__(self, sqlmapapiurl, adminid):
        self.sqlmapapiurl = sqlmapapiurl #SQLMAP API服务地址
        self.adminid = adminid #SQLMAP API adminid
        self.mysql = Mysql(conf.db_host, conf.db_port, conf.db_user, conf.db_pass, conf.db_name)
        self._handle_result()
        
    #获取当前任务列表
    def _get_task_list(self):
        log('_get_task_list', 'begin _get_task_list')
        checkurl = self.sqlmapapiurl + '/admin/' + self.adminid + '/list';
        resp = json.loads(do_get(checkurl))
        log('_get_task_list', 'end _get_task_list')
        return resp['tasks']
    
    #漏洞结果入库
    def _item2db(self, taskid):
        log('_item2db', 'begin _item2db')
        dataurl = self.sqlmapapiurl + '/scan/' + taskid + '/data';
        resp = json.loads(do_get(dataurl))
        if data != []:
            dset = "data='%s', sqli=1" % base64.b64encode(str(data[0]))
        else:
            dset = "sqli=0"
        where = "taskid='%s'" % taskid
        self.mysql.update('sub_sqli', dset, where)   
        log('_item2db', 'end _item2db')
        return
    
    #删除已完成的任务
    def _delete_task(self, taskid):
        log('_delete_task', 'begin _delete_task')
        deleteurl = self.sqlmapapiurl + '/task/' + taskid + '/delete'
        do_get(deleteurl)
        log('_delete_task', 'end _delete_task')
        return
    
    #从数据库中删除无漏洞条目
    def _delete_no_sqli(self):
        log('_delete_no_sqli', 'begin _delete_no_sqli')
        self.mysql.delete('sub_sqli', 'sqli=0')
        log('_delete_no_sqli', 'end _delete_no_sqli')
        return
    
    #处理任务结果
    def _handle_result(self):
        log('handle_result', 'begin handle_result')
        tasklist = self._get_task_list()
        for taskid, state in tasklist.items():
            if state == 'terminated':
                self._item2db(taskid)
                self._delete_task(taskid)
        self._delete_no_sqli()
        log('handle_result', 'end handle_result')
        return
    
    #获取漏洞结果
    def get_sqli_result(self):
        return self.mysql.select(('url', 'body', 'data'), 'sub_sqli', 'sqli=1')
        
    #获取正在进行的任务列表
    def get_scaning_list(self):
        return self.mysql.select(('url', 'body'), 'sub_sqli', 'sqli not in (0, 1)')
    
    #强行善后
    def tasks_clean(self):
        tasklist = self._get_task_list()
        for taskid in tasklist:
            self._delete_task(taskid)
        self.mysql.delete('sub_sqli', 'sqli not in (1)')
        return
        
    

