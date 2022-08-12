"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2022/8/6 16:45
# @Author:YiShouquan
# @File:app.py
# @Update:
"""
from datetime import datetime

from flask import Flask, request, render_template
from flask import session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager

from Python_Flask_StudentsInfo.SqliteCreate import BASE_DIR, create_connection, create_table, check_table, \
    InsertInto_Batch, Select_all_data
from Python_Flask_StudentsInfo.db_sql import engine, StudentInfo, oper_first

app = Flask(__name__, template_folder='templates')
# 强制性必须填写secret_key
app.config['SECRET_KEY'] = 'Miss Gao students learn information materials'
bootstrap = Bootstrap(app)
manager = Manager(app)
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


@app.route('/login/students_info', methods=['GET', 'POST'])
def students_info():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['number'] = request.form['number']
        session['email'] = request.form['email']
        session['teacher'] = request.form['teacher']
        session['class_type'] = request.form['class_type']
        session['tuition'] = request.form['tuition']
        # list = []
        # print({
        #     "name": session['name'],
        #     "number": session['number'],
        #     "email": session['email'],
        #     'teacher': session['teacher'],
        #     "class_type": session['class_type'],
        #     'tuition': session['tuition']})
        # 引入创建py和数据库连接的sessionmaker函数
        # from sqlalchemy.orm import sessionmaker
        # Session = sessionmaker(engine)()
        # # 新增测试数据
        # stu_info = StudentInfo(name=session['name'],
        #                        phone=session['number'],
        #                        email=session['email'],
        #                        teacher=session['teacher'],
        #                        class_type=session['class_type'],
        #                        tuition=session['tuition'])
        # Session.add(stu_info)
        # # 结束之后，必须要提交
        # Session.commit()
        # # 查询数据
        # stu_info1 = oper_first(Session)
        # print(stu_info1)
        # Session.close()  # 关闭会话
        database = BASE_DIR + r'/Python_Flask_StudentsInfo/StudentInfo.db'

        sql_create_stu_table = """CREATE TABLE IF NOT EXISTS StudentInfo (
                                            ID INTEGER Primary KEY,
                                            NAME VARCHAR(20) not null,
                                            PHONE INTEGER,
                                            EMAIL TEXT,
                                            TEACHER TEXT,
                                            CLASSTYPE TEXT,
                                            TUITION INTEGER
                                        );"""

        # 创建数据库连接
        conn = create_connection(database)
        # 获取该数据库的游标
        cursor = conn.cursor()

        # 创建数据表
        if conn is not None:
            # 创建students_info表
            create_table(conn, sql_create_stu_table)

        else:
            print("Error! cannot create the database connection.")

        if check_table(database, 'StudentInfo') == True:
            X = InsertInto_Batch(cursor, 'StudentInfo',
                                 name=session['name'], phone=session['number'],
                                 email=session['email'], teacher=session['teacher'],
                                 class_type=session['class_type'], tuition=session['tuition'])
            print(X)
            Y = Select_all_data(cursor, 'StudentInfo')
            print(Y)
            # 关闭Cursor:
            cursor.close()

            # 提交事务:
            conn.commit()

            # 关闭Connection:
            conn.close()

    return render_template('bootstrap_user.html', method=request.method)


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
    app.run(port=8000, debug=True, host='0.0.0.0')
