#!/usr/bin/env python
#coding:utf-8

from flask import Flask

DEBUG = True
SECRET_KEY = '7\xe9\xcf\x17\x11\x92I^"|\xbc\x85\xc8\xc1u\x18\xbb\xec\xc9\xe2\xbb,\x9fX'
app = Flask(__name__)
app.config.from_object(__name__)

if __name__ == '__main__':
    app.run()
