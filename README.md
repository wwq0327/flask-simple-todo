简明TODO应用

基于flask框架的一个小应用。这个简不简单我就不清楚了，反正我是写出来了，哈哈。

## 缘起

看着高手们用不同的Web框架实现了这个小应用，而我这样的新手正在学习Flask，就拿来练下手了，他们用不同的框架所实现的应用：

- web.py ~~ http://simple-is-better.com/news/309
- Uliweb ~~ http://limodou.github.com/uliweb-doc/basic.html
- Bottle ~~ https://bitbucket.org/ZoomQuiet/bottle-simple-todo

## 运行需求

- python 2.5+
- flask 0.7
- flask-sqlalchemy
- flask-script
- flask-wtf

上面提到的flask插件，可用 ``easy_install`` 进行安装

## 本应用安装及运行

**初始化数据库**

进入Python Shell，执行下面两行代码：::

    from todo import db
    db.create_all()

**启动**

``python run.py runserver``

**使用**

在浏览器中打开 http://127.0.0.1:5000

## 在线教程

[flask-simple-todo v0.1 documentation](http://flask-simple-todo.readthedocs.org/en/latest/?redir)
