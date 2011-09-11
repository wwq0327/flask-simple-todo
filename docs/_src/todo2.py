#!/usr/bin/env python
#coding:utf-8

from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

DEBUG = True
SECRET_KEY = '7\xe9\xcf\x17\x11\x92I^"|\xbc\x85\xc8\xc1u\x18\xbb\xec\xc9\xe2\xbb,\x9fX'
SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.sqlite'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
db.init_app(app)

class Todo(db.Model):
    '''数据模型'''
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    posted_on = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.Boolean(), default=False)

    def __init__(self, *args, **kwargs):
        super(Todo, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<Todo '%s'>" % self.title

    def store_to_db(self):
        '''保存数据到数据库'''
        
        db.session.add(self)
        db.session.commit()

    def delete_todo(self):
        '''删除数据'''
        
        db.session.delete(self)
        db.session.commit()


if __name__ == '__main__':
    app.run()
