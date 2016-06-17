#encoding=utf-8
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

from lib.sqlimanage import SqliManage
import config.config as conf

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sqli')
def sqli_html():
    sqlimanage = SqliManage(conf.sqlmapapi_url, conf.admin_id)
    sqlimanage.handle_result()
    sqliresult = sqlimanage.get_sqli_result()  
    return render_template('sqli.html', sqliresult=sqliresult)

if __name__ == '__main__':
    app.run()

