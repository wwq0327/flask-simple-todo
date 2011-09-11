.. 0.1 documentation master file, created by
   sphinx-quickstart on Thu Jul  7 09:01:38 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Todo for Flask's documentation!
===================================================

介绍 Todo
=================
看着高手们用不同的Web框架实现了这个小应用，而我这样的新手正在学习Flask，就拿来练下手了，他们用不同的框架所实现的应用：

- web.py版 http://simple-is-better.com/news/309
- Uliweb版 http://limodou.github.com/uliweb-doc/basic.html
- Bottle版 https://bitbucket.org/ZoomQuiet/bottle-simple-tod

TODO具备的功能：

- 实现任务的追加，修改，删除功能。
- 完成或重置任务功能。

使用了 `Flask-SQLAlchemy`_ 扩展，数据库用的是 ``sqlite`` ，为因为他很小型，在做开发的时候用着不错。下面就开始一步步的构建这个程序。

初始准备：创建目录
===============================
web应用，多不是一个单一的程序就能解决问题的，创建一个目录，将所有内容放在这个目录中，方便管理。本应用目录为：::

	/todo
	   /static
	   /templates

``static`` 目录用于存放如img、js、css等文件，这些文件能通过HTTP直接访问， ``templates`` 用于存放Flask应用所需要的 ``jinja2`` 模板文件。我们把所有的模板文件都放在此目录中。

构建应用程序代码
===============================
当我们准备好了应用的模式后，就可以创建应用的模块了。本例中，我把它叫做 ``todo.py`` ，并把它放在 todo 目录中。首先我们要导入一些Flash必用的模块和配置。如果是一个小应用的话，配置可直接放在模块中，如果应用比较大，可使用单独的文件进行配置，然后再导入主模块中即可。

导入模块
---------------
::

	from flask import Flask

这里只导入了一个 ``Flask`` 模块，只需要这个一个模块，程序就能运行起来了，当然对于更复杂的应用，光这一个模块是不够的，待会遇到之时，我们再进行导入。

配置
---------------
::

	DEBUG = True
	SECRET_KEY = 'secret_key'

配置选项一，开启服务器的debug支持，每次修改服务器都会自动重启，如果出现问题的话，还会提供一个有用的调试器。Debug标志用来指示是否开启交互debugger。永远不要在生产环境下开始 debug标志，因为这样会允许用户在服务器上执行代码！

配置选项二，我们需要设置 secret_key 来确保客户端Session的安全。合理的设置这个值，而且越复杂越好。Python中的 ``os.urandom`` 可方便获得： ::

        In [1]: import os
        In [2]: os.urandom(24)
        Out[2]: '7\xe9\xcf\x17\x11\x92I^"|\xbc\x85\xc8\xc1u\x18\xbb\xec\xc9\xe2\xbb,\x9fX'

将产生的字符串复制替换掉 ``secret_key`` 即可

配置初始化
---------------
由于只是一个小应用，初始化我们放在同一文件中完成 ::

       app = Flask(__name__)
       app.config.from_object(__name__)

``from_object`` 会识别给出的对象（如果是一个字符串，它会自动导入这个模块），然后查找所有已定义的大写变量。在我们这个例子里，配置在几行代码前。你也可以把它移动到一个单独的文件中。					

开启服务器
-----------------

要启动服务器，在最后加入这样的代码：::

	if __name__ == '__main__':
	    app.run()

现在就能启动服务器了：::

	python todo.py

启动后的提示是这样的：::

        * Running on http://127.0.0.1:5000/
        * Restarting with reloader...

这时就能在浏览器中打开这个网址了，不过此时访问服务器，你会得到一个404页面没找到的错误。因为我们还没有创建视图。

第一步代码
------------------
第一步后，代码像这样：

.. literalinclude:: _src/todo1.py
   :linenos:

创建数据库
==================

创建数据库，分为三步： 配置数据库，初始化数据库和数据库模型，这里以 `Flask-SQLAlchemy`_ 为例。

配置
-------------------------
配置数据库，只需要模块的配置部分加入下面这行代码：::

	SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.sqlite'

这是一个关于 sqlite 的配置，其它配置，可参看 `这里 <http://packages.python.org/Flask-SQLAlchemy/config.html#connection-uri-format>`_ 。

创建数据库实例
--------------------------
``SQLAlchemy`` 模块导入：::

         from flaskext.sqlalchemy import SQLAlchemy

在前面的 ``app`` 配置后面加入下面两行代码：::

	 db = SQLAlchemy(app)
	 db.init_app(app)

创建数据模型
----------------
数据模型：::

	class Todo(db.Model):
	    '''数据模型'''
	        
	    id = db.Column(db.Integer, primary_key=True)
	    title = db.Column(db.String(255), nullable=False)
	    posted_on = db.Column(db.Date, default=datetime.utcnow)
            status = db.Column(db.Boolean(), default=False)

模型型初始化：::

	    def __init__(self, *args, **kwargs):
	        super(Todo, self).__init__(*args, **kwargs)
  
            def __repr__(self):
                return "<Todo '%s'>" % self.title

模型增补数据操作功能：::

    def store_to_db(self):
        '''保存数据到数据库'''
        
        db.session.add(self)
        db.session.commit()

    def delete_todo(self):
        '''删除数据'''
        
        db.session.delete(self)
        db.session.commit()


初始化数据库
------------------
进入python命令行，然后：::

	from todo import db
	db.create_all()

如果没问题的话，你可以在当前目录中看到数据库文件了。如果需要重建数据表，可使用 ``db.drop_all()`` 清除数据。

第二步代码
------------------
第二步后，代码像这样：

.. literalinclude:: _src/todo2.py
   :linenos:

表单
==================

表单引入模块：::

	from flaskext.wtf import Form, TextField, SubmitField, required, ValidationError

表单代码：::

	class TodoForm(Form):
	    '''表单'''
	        
	    title = TextField(u"内容", validators=[required(message=u"任务内容")])

只是一个表单，当然也可以直接放到html中.定义好的表单，可用如下方式进行调用：::

	{{ form.title.label }} {{ form.title }}

将其写入HTML的 ``<form></form`` 即可。        

视图
==================
现在数据库连接已能正常工作了，这步就开始写视图函数。五个功能视图及一个404视图。

route
---------------
装饰器 ``flask.Flask.route`` 用于绑定一个函数到一个网址。但是它不仅仅只有这些!你可以构造动态的网址并给函数附加多个规则.

这里是一个例子：::

	@app.route('/')
	def index():
	    return 'Index Page'
	    	    
	@app.route('/hello')
	def hello():
	    return 'Hello World'

一个函数可对应我个视图。如 ``index`` 视图，也可以再加个 ``@app.route('/index')`` ,这样 ``/`` 和 ``/index`` 都会调用 ``index`` 函数。每个视力都必须 ``return`` 语句返回调用。

主视图
---------------
主视图代码如下：
::

	@app.route('/', methods=['GET', 'POST'])
	def index():
	    todo = Todo.query.order_by('-id')
            form = TodoForm(request.form)
	    if request.method == 'POST' and form.validate_on_submit():
                t = Todo(title=form.title.data)
		try:
                    t.store_to_db()
		    flash(u"添加成功")
                    return redirect(request.args.get('next') or url_for('index'))
        	except:
                    flash(u'存储失败！')
             
            return render_template('index.html', todo=todo, form=form)

编辑视图
---------------

::

	@app.route('/<int:id>/edit', methods=['GET', 'POST'])
	def edit(id):
            todo = Todo.query.filter_by(id=id).first()
    	    form = TodoForm(title=todo.title)
	    if request.method == 'POST' and form.validate_on_submit():
                Todo.query.filter_by(id=id).update({Todo.title:request.form['title']})
                db.session.commit()
                flash(u"记录编辑成功")
                return redirect(url_for('index'))
 
            return render_template('edit.html', todo=todo, form=form)

删除视图
---------------
::

	def tdel(id):
	    todo = Todo.query.filter_by(id=id).first()
	    if todo:
                todo.delete_todo()
    	    flash(u"记录删除成功")
    	    return redirect(url_for('index'))

完成视图
---------------
::

	@app.route('/<int:id>/done')
	    def done(id):
	    todo = Todo.query.filter_by(id=id).first()
	    if todo:
                Todo.query.filter_by(id=id).update({Todo.status:True})
        	db.session.commit()
                flash(u"任务完成")

	    return redirect(url_for('index'))

重置视图
---------------
::

	@app.route('/<int:id>/redo')
	def redo(id):
	    todo = Todo.query.filter_by(id=id).first()
    	    if todo:
                Todo.query.filter_by(id=id).update({Todo.status:False})
     		flash(u"记录重置成功")
		db.session.commit()
		
            return redirect(url_for('index'))

404视图
---------------
::

	@app.errorhandler(404)
	def page_not_found(error):
	    return render_template('page_404.html'), 404

整个代码
---------------
.. literalinclude:: _src/todo3.py
   :linenos:

模版
===============

base.html
--------------------
.. literalinclude:: ../templates/base.html
   :linenos:

index.html
--------------------
.. literalinclude:: ../templates/index.html
   :linenos:

edit.html
--------------------
.. literalinclude:: ../templates/edit.html

page_404.html
--------------------
.. literalinclude:: ../templates/page_404.html

增加页面样式
====================
.. literalinclude:: ../static/style.css
   :linenos:

.. _Flask-SQLAlchemy: http://packages.python.org/Flask-SQLAlchemy/
