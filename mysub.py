#encoding=utf-8
import json
import time
import config.config as conf
from urlparse import urlparse
from lib.http import do_get, do_post
from lib.db import Mysql

#SQLMAP API服务地址
sqlmapapiurl = "http://127.0.0.1:9462"

#日志记录
def log(tag, message):
    f = open('/tmp/mysub/mysub.log', 'a+')
    f.write('[%s] %s: %s\n' % (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), tag, message))
    f.close()
    return

#sqli任务初入库
def task2db(taskid, url, body):
    mysql = Mysql(conf.db_host, conf.db_port, conf.db_user, conf.db_pass, conf.db_name)
    mysql.insert('sub_sqli', ('taskid', 'url', 'body'), (taskid, url, body))
    return

#创建SQLI任务
def send2sqlmap(url, user_agent='', cookie='', body=''):
    newurl = sqlmapapiurl + '/task/new'
    resp = json.loads(do_get(newurl))
    taskid = resp['taskid']
    log('send2sqlmap', 'task is created. id : %s' % taskid)
    data = {}
    data['url'] = url
    if cookie != '' and cookie != []:
        data['cookie'] = cookie[0]
    data['headers'] = 'User-Agent: ' + user_agent[0]
    if body != '':
        data['data'] = body
    starturl = sqlmapapiurl + '/scan/' + taskid + '/start'
    do_post(starturl, user_agent, cookie, json.dumps(data))
    log('send2sqlmap', 'task is started. id : %s' % taskid)
    task2db(taskid, url, body)
    return

#检测该请求是否需要进行SQLI测试
def is_need_sqli_test(url, body):
    parsedurl = urlparse(url)
    if parsedurl.query == '' and body == '':
        return False
    return True

#sql注入测试模块
def sqli_test(req):
    user_agent = req.getHeader("User-Agent")
    cookie = req.getHeader("Cookie")
    body = req.body
    url = req.url
    if req.method == 'CONNECT':
        url = 'https://' + url
    if is_need_sqli_test(url, body):
        log('sqli_test', 'target url : %s' % url)
        send2sqlmap(url, user_agent, cookie, body)
    return

def proxy_mangle_request(req):
    sqli_test(req)
    return req

def proxy_mangle_response(res):
    return res

