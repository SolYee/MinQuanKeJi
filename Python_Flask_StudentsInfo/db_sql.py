"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2022/8/5 12:28
# @Author:YiShouquan
# @File:db_sql.py
# @Update:
"""
"""
参考链接地址：
https://github.com/pomegranate66/py_note/blob/2349e41a986e0d505719bccc12986708974c8667/Flask/Flask%E6%95%B0%E6%8D%AE%E5%BA%93.md
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 依次导入常用的数据类型
from sqlalchemy import create_engine, Column, Integer, String, Float, DECIMAL, Boolean, Date, DateTime, Time, Text, Enum
# 从sqlalchemy的方言模块dialects导入mysql专有的LONGTEXT,长文本类型
from sqlalchemy.dialects.mysql import LONGTEXT
# 在python3.x中有enum模块
import enum
# 导入时间
from datetime import datetime, date, time
# 用`declarative_base`根据`engine`创建一个ORM基类。
from sqlalchemy.ext.declarative import declarative_base

# 引入创建py和数据库连接的sessionmaker函数
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 准备连接数据库基本信息
# 代表哪一台计算机，ip地址是多少
HOSTNAME = '127.0.0.1'
# 端口号
PORT = '3306'
# 数据库的名字，连接那个数据库
DATABASE = 'first_sqlalchemy'
# 数据库的账号和密码
USERNAME = 'root'
PASSWORD = 'root'
# 按照要求组织成一定的字符串
# '数据库类型+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名'
"""配置参数"""
'''sqlalchemy的配置参数'''
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://{username}:{pwd}@{host}:{port}/{db}?charset=utf8' \
        .format(username=USERNAME, pwd=PASSWORD, host=HOSTNAME, port=PORT, db=DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# 开启事务自动提交
# '''设置sqlalchemy自动跟踪数据库''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

'''创建数据库 sqlalchemy 工具对象'''
db = SQLAlchemy(app)
# 创建数据库引擎
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

"""
    创建数据库模型类(继承 sqlalchemy 工具对象中的Model类),一个模型类对应一张模型表
    数据库表名的常见规范：
        (1) 数据库名缩写_表名   (2) tbl_表名
"""

'''
    relationship()把两个表关联在一起，不添加也是可以的，根据自己的需求
    backref : 在关系的另一模型中添加反向引用
               相当于给要关联的表添加一个role属性
               不添加也是可以的，根据自己的需求
'''


# 2.创建ORM模型
class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(11), unique=True)
    email = Column(String(128), unique=True)
    teacher = Column(String(128))
    class_type = Column(String(128))
    tuition = Column(String(128))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)  # onupdate是在数据更新的时候才会起作用，插入数据时候不起作用

    def __repr__(self):
        return "<User(uname: %s)>" % self.uname


# user = db.relationship("User", backref="role")  # 从模型类中

# # 创建连接,如果运行之后，输入1则连接成功
# with engine.connect() as con:
#     rs = con.execute('SELECT 1')
#     print(rs.fetchone())

Base = declarative_base(engine)


class StudentInfo(Base):
    __tablename__ = 'StudentInfo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(11), unique=True)
    email = Column(String(128), unique=True)
    teacher = Column(String(128))
    class_type = Column(String(128))
    tuition = Column(String(128))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)  # onupdate是在数据更新的时候才会起作用，插入数据时候不起作用


"""Column常用数据类型
常用的数据类型，一共是有11个。

注：在SQLAlchemy中不存在double数据类型，使用DECIMAL类型替代

让我们来分别看下这11个数据类型都有哪些？

Integer：整型，映射到数据库中是int类型。

Float：浮点类型，映射到数据库中是float类型。他占据的32位。

浮点类型，有可能会造成精度丢失，特别是在money方面，不可原谅。

Double（SQLAlchemy中没有，代替品为DECIMAL）：双精度浮点类型，映射到数据库中是double类型，占据64位

String：可变字符类型，映射到数据库中是varchar类型.

Boolean：布尔类型，映射到数据库中的是tinyint类型。

DECIMAL：定点类型。是专门为了解决浮点类型精度丢失的问题的。在存储money相关的字段的时候建议大家都使用这个数据类型。并且这个类型使用的时候需要传递两个参数，第一个参数是用来标记这个字段总能能存储多少个数字，第二个参数表示小数点后有多少位。

Enum：枚举类型。指定某个字段只能是枚举中指定的几个值，不能为其他值。在ORM模型中，使用Enum来作为枚举。
    # 枚举另外一种写法，导入enum模块，定义枚举类
    class TagEnum(enum.Enum):
        python = "PYTHON"
        flask = 'FLASK'
        django = 'DJANGO'
Date：存储时间，只能存储年月日。映射到数据库中是date类型。在Python代码中，可以使用datetime.date来指定。

DateTime：存储时间，可以存储年月日时分秒毫秒等。映射到数据库中也是datetime类型。在Python代码中，可以使用datetime.datetime来指定。

Time：存储时间，可以存储时分秒。映射到数据库中也是time类型。在Python代码中，可以使用datetime.time来指定

    注意区分Date/DateTime/Time的储存信息！！！

Text：存储长字符串。一般可以存储6W多个字符

LONGTEXT：长文本类型，映射到数据库中是longtext类型（不过这个只有mysql有，orcale没有）


Column常用约束参数
在给数据库表指定key的时候，必然要给它们添加，例如：不可空，字节长度等等的限制，这就需要约束参数的出场了。常用的约束参数一共有7种

常见约束参数
约束参数	            描述，功能
primary_key	    True设置某个字段为主键
autoincrement	True设置这个字段为自动增长的
default	        设置某个字段的默认值。在发表时间这些字段上面经常用
nullable	    指定某个字段是否为空。默认值是True，就是可以为空
unique	        指定某个字段的值是否唯一。默认是False。
onupdate	    在数据更新的时候会调用这个参数指定的值或者函数。在第一次插入这条数据的时候，不会用onupdate的值，只会使用default的值。常用于是update_time字段（每次更新数据的时候都要更新该字段值）。
name	        指定ORM模型中某个属性映射到表中的字段名。如果不指定，那么会使用这个属性的名字来作为字段名。这个参数也可以当作位置参数，在第1个参数来指定。
"""

# 将Base上的ORM类模型对应的数据表都删除
# Base.metadata.drop_all()
# 创建Base上的ORM类到数据库中成为表
# Base.metadata.create_all()


# # 新增数据到表news中
# session = sessionmaker(engine)()
# 注意float出现的精度丢失问题      is_delete,布尔类型true：1，false:0
# news1 = News(price1=1000.0078,price2=1000.0078,title='测试数据',is_delete=True,tag1="PYTHON",tag2=TagEnum.flask,   	create_time1=date(2018,12,12),create_time2=datetime(2019,2,20,12,12,30),create_time3=time(hour=11,minute=12,second=13),content1="hello",content2 ="hello   hi   nihao")
#
#
# session.add(news1)
# session.commit()


from sqlalchemy.orm import aliased

# 取别名
a1 = aliased(StudentInfo)


def oper_first(session):
    return session.query(a1).first()


def oper_all(session):
    return session.query(a1).all()
