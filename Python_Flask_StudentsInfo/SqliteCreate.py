"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2022/8/11 8:59
# @Author:YiShouquan
# @File:SqliteCreate.py
# @Update:
"""
import logging
import sqlite3
from sqlite3 import Error
import os
from typing import Union

BASE_DIR: Union[bytes, str] = os.path.dirname(os.path.abspath(__file__))


def check_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = '''SELECT tbl_name FROM sqlite_master WHERE type = 'table' '''
    cursor.execute(sql)
    values = cursor.fetchall()
    tables = []
    for v in values:
        tables.append(v[0])
    if table_name not in tables:
        return False  # 可以建表
    else:
        return True  # 不能建表


def create_connection(db_file):
    """ 创建一个到SQLite数据库的数据库连接由db_file指定
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(cursor, create_table_sql):
    """ 从create_table_sql语句创建一个表
    :param cursor: 获取该数据库的游标
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        # c = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)


# def main():
#     database = BASE_DIR + r'/Python_Flask_StudentsInfo/StudentInfo.db'
#
#     sql_create_stu_table = """CREATE TABLE IF NOT EXISTS repo (
#                                     ID INTEGER Primary KEY,
#                                     Name VARCHAR(20) not null,
#                                     PHONE INTEGER,
#                                     EMAIL TEXT,
#                                     TEACHER TEXT,
#                                     CLASSTYPE TEXT,
#                                     TUITION INTEGER
#                                 );"""
#
#     # create a database connection
#     conn = create_connection(database)
#
#     # create tables
#     if conn is not None:
#         # create students_info table
#         create_table(conn, sql_create_stu_table)
#
#     else:
#         print("Error! cannot create the database connection.")


def InsertInto_Batch(cursor, tablename, name, phone, email, teacher, class_type, tuition):
    # # 执行单条数据插入，并返回操作行数
    sql = f"INSERT INTO {tablename} (NAME, PHONE ,EMAIL ,TEACHER ,CLASSTYPE ,TUITION) VALUES ({name},{phone},{email},{teacher},{class_type},{tuition})"
    batchInsert = cursor.execute(sql)
    logging.info(f"插入了{batchInsert.rowcount}条数据:"
                 f"[{'name': {name},'phone': {phone},'email': {email},'teacher': {teacher},'class_type': {class_type},'tuition': {tuition}}]")
    return f"[{'name': {name},'phone': {phone},'email': {email},'teacher': {teacher},'class_type': {class_type},'tuition': {tuition}}]"
    # # 关闭Cursor:
    # cursor.close()
    #
    # # 提交事务:
    # conn.commit()
    #
    # # 关闭Connection:
    # conn.close()


def Select_all_data(cursor, tablename):
    cursor.execute(f"select * from {tablename}")
    # 提取查询到的数据
    return cursor.fetchall()

