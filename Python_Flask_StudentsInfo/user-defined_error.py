"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2022/8/5 12:21
# @Author:YiShouquan
# @File:user-defined_error.py
# @Update:
"""
from flask import Flask, render_template

app = Flask(__name__)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500