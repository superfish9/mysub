#encoding=utf-8
import sys
import json
import base64
from http import do_get, do_post
from db import Mysql

sys.path.append('..')
import config.config as conf

#sql注入管理模块
class SqliManage(object):
    def __init__(self, sqlmapapiurl, adminid):
        self.sqlmapapiurl = sqlmapapiurl #SQLMAP API服务地址
        self.adminid = adminid #SQLMAP API adminid
        self.mysql = Mysql(conf.db_host, conf.db_port, conf.db_user, conf.db_pass, conf.db_name)
        
    #获取当前任务列表
    def _get_task_list(self):
        checkurl = self.sqlmapapiurl + '/admin/' + self.adminid + '/list';
        resp = json.loads(do_get(checkurl))
        return resp['tasks']
    
    #漏洞结果入库
    def _item2db(self, taskid):
        dataurl = self.sqlmapapiurl + '/scan/' + taskid + '/data';
        resp = json.loads(do_get(dataurl))
        if data != []:
            dset = "data='%s', sqli=1" % base64.b64encode(data[0])
        else:
            dset = "sqli=0"
        where = "taskid=%s" % taskid
        self.mysql.update('sub_sqli', dset, where)   
        return
    
    #删除已完成的任务
    def _delete_task(self, taskid):
        deleteurl = self.sqlmapapiurl + '/task/' + taskid + '/delete'
        do_get(deleteurl)
        return
    
    #从数据库中删除无漏洞条目
    def _delete_no_sqli(self):
        self.mysql.delete('sub_sqli', 'sqli=0')
        return
    
    #处理任务结果
    def handle_result(self):
        tasklist = self._get_task_list()
        for taskid, state in tasklist.items():
            if state == 'terminated':
                self._item2db(taskid)
                self._delete_task(taskid)
        self._delete_no_sqli()
        return
    
    #获取漏洞结果
    def get_sqli_result(self):
        return self.mysql.select(('url', 'body', 'data'), 'sub_sqli', 'sqli=1')
        
        
    

