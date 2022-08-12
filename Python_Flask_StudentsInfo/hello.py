"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2022/8/5 10:46
# @Author:YiShouquan
# @File:hello.py
# @Update:
"""
# hello.py

from datetime import datetime
from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)




if __name__ == '__main__':
    """
    每个脚本包含__main__函数，当该模块被直接执行的时候，__main__等于文件名（包含后缀.py）
    如果被引入其它模块，则该模块__main__等于模块名称（不包含后缀.py）
    ‘__main__’始终指当前执行模块名称（包含后缀.py）
    Flask Web 开发服务器也可以通过编程的方式启动：调用 app.run() 方法
        在没有 flask 命令的旧版 Flask 中，若想启动应用，要运行应用的主脚本。主脚本的尾部包含下述代码片段：
    --host
        --host 参数特别有用，它告诉 Web 服务器在哪个网络接口上监听客户端发来的连接。
        
        默认情况下，Flask 的 Web 开发服务器监听 localhost 上的连接，因此服务器只接受运行服务器的计算机发送的连接。
        
        下述命令让 Web 服务器监听公共网络接口上的连接，因此同一网络中的其他计算机发送的连接也能接收到：
    """
    app.run(port=5000, debug=True, host='0.0.0.0')
