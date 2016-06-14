#encoding=utf-8
from flask import render_template
from flask import Flask
app = Flask(__name__)

from lib.sqlimanage import SqliManage
import config.config as conf

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/sqli')
def sqli_html():
    sqlimanage = SqliManage(conf.sqlmapapi_url, conf.admin_id)
    sqliresult = sqlimanage.get_sqli_result()  
    return render_template('sqli.html', sqliresult=sqliresult)

if __name__ == '__main__':
    app.run()

