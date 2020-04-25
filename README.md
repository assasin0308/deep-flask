# deep-flask 

##### --version=0.10.1 

##### flask + gunicorn + nginx

### 1. installation

```python
# pip install flask

# flask-plugin
flask-sqlalchemy # 操作数据库
flask-mail # 邮件
flask-migrate # 管理迁移数据库
flask-WFT # 表单
flask-script # 插入脚本
flask-Login # 认证用户状态
flask-RESTful # 开发 REST api工具
flask-Bootstrap # 集成前段 Twitter Bootstrap框架
flask-Moment # 本地化日期和时间

# document 
# https://dormousehole.readthedocs.io/en/latest/    Chinese
# https://flask.palletsprojects.com/en/1.1.x/       English
```

### 2. virtualenv config

```shell
pip install virtualenv
pip install virtualenvwrapper
# 创建目录存放虚拟环境
mkdir $HOME/.virtualenvs
# 打开~/.bashrc文件,并添加:
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
# 运行
source ~/.bashrc

pip freeze > requirements.txt
pip install -r requirements.txt
```

### 3. hello world

```python
# coding:utf-8
from flask import Flask,request,\
    render_template,make_response,current_app
from werkzeug.routing import BaseConverter

app = Flask(
    __name__,
    static_url_path='/python', # 访问静态资源的url前缀,默认 static
    static_folder='jingtai', # 静态文件存放目录,默认 static
    template_folder='muban', # 模板文件目录 ,默认 templates
)   # 同 app = Flask('__main__')

# 配置参数
# 1. 使用配置文件
# 使用配置文件配置参数
    # 1. app.config.from_pyfile("config.cfg")

    # class Config(object):
    #     DEBUG = True
    #     NAME = 'assasin'
    #
    # app.config.from_object(Config)
    # 使用对象配置参数  项目推荐
    # 2. app.config.from_object(Config)
    # 3. app.config.from_envvar()
    # 4. 直接操作config的字典对象
    # app.config["DEBUG"] = True


# 路由配置
# 查看所有路由信息: app.url_map
# 路由转换器 @app.route('/goods/<int:goods_id>')



@app.route('/')
def index():
    # 读取配置参数
    # 1. 直接从全局对象app的config字典中取值
    # app.config["DEBUg"]
    # app.config.get("NAME")
    # 2. 通过current_app获取
    # print(current_app.config.get('NAME'))
    return 'hello world'


# 路由转换器
# @app.route('/goods/<int:goods_id>') #只接受整型
@app.route('/goods/<goods_id>') # 接受除 '/' 以外的任何字符
def goods_detail(goods_id):
    return 'goods_id is: %s' % goods_id

#------------- 自定义路由转换器 --------------------------------------

# 自定义路由转换器 使用类的方式 继承 werkzeug
    #  1. from werkzeug.routing import BaseConverter
    # class RegxConvert(BaseConverter):
    # 
    #     def __init__(self,url_map,regex):
    #         # 调用父类的构造方法
    #         super(RegxConvert,self).__init__(url_map)
    #         self.regx = regex
    # 2. 将自定义的转换器添加至路由中
    # app.url_map.converters['regx'] = RegxConvert

@app.route("/send_sms/<regx(r'1[34578]\d{9}'):mobile>")
def send_sms(mobile):
    return 'send sms to %s ' % mobile

#---------------------------------------------------------------------



@app.route('/post_only',methods=['POST'])
def post_only():
    return 'post only page'



if __name__ == '__main__':
    # app.run() 参数配置:
    # host: '0.0.0.0' 默认 127.0.0.1
    # port: 5001 默认 5000
    # debug: True/False 开启/关闭debug模式
    print(app.url_map) # 查看所有路由信息
    app.run(host='0.0.0.0',debug=True)


```

### 4. request

```python
from flask import Flask,request,\
    render_template,make_response,current_app,abort,Response


app = Flask(__name__)

# request 常用属性说明
#------------------------------------------------------------------------------
#        属 性              说 明                            类 型
#        data       记录请求的数据,并转化为字符串              *
#        form       记录请求中的表单数据                    MultiDict
#        args       记录请求中的查询参数                    MultiDict
#        cookies    记录请求中的cookie信息                  Dict
#        headers    记录请求中的报文头                      EnvironHeaders
#        method     记录请求使用的HTTP方法                  GET/POST
#        url        记录请求的url地址                       String
#        files      记录请求上传的文件                        *
#------------------------------------------------------------------------------


@app.route('/index',methods=['GET','POST'])
def index():
    return 'request study'

# with 上下文管理器
# with open('./README.md','wb') as f:
#     f.write('hello assasin')


# abort 使用 立即终止视图函数的执行,并返回特定信息
# from flask import abort
# from flask import Response
@app.route('/login')
def  login():
    name = ''
    pwd = ''
    if name != 'assasin' or pwd != 'admin':
        abort(400)
        # resp = Response("login failed")
        # abort(resp)
        # abort(标准的http状态码)
        # abort(传递响应体信息)

    return 'login success'


# 自定义错误处理机制
@app.errorhandler(404)
def not_found(error):
    return ' %s' % error ,404


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
```

### 5.  response & cookie & session & hook

```python
from flask import Flask,request,\
    render_template,make_response,current_app,jsonify,session,url_for,g


app = Flask(__name__)

@app.route('/')
def index():
    # 自定义response
    # 1. 使用元组,返回自定义响应信息
    #        响应体     状态码    响应头
    # return 'index page', 400,    [("name","shibin"),("age",28)]
    # return 'index page', 666,    {"name":"shibin","city":"beijing"}
    # 状态码可自定义,可传字符串
    # return 'index page', "666 success", {"name": "shibin", "city": "beijing"}
    # 也可不传响应头
    # return 'index page', "666 success"
    # 2. 借助 make_response  构造响应信息
    resp = make_response("index page2 ") # 设置响应体
    resp.status = "666 shibin" # 设置状态码
    resp.headers['city'] = "beijing" # 设置响应头
    return resp

# 构造json格式返回
@app.route('/json')
def json():
    data = {
        "name" : "shibin",
        "age" : 25
    }
    # json_str = json.dumps(data)
    # return json_str,200,{"Content-Type" :"application/json"}
    # jsonify() 将数据转为json格式,并设置响应头格式为: "Content-Type" :"application/json"
    # return jsonify(data)
    return jsonify(city="beijing",country="china")


# ----------------------  Cookie 操作---------------------------------
@app.route('/set_cookie')
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("name","shibin") #  默认临时有效,浏览器关闭即可失效
    resp.set_cookie("city","beijing",max_age=3600) #  max_age 设置有效期 单位:秒
    resp.headers['Set-Cookie'] = 'city2=xian; Expires=Wed, 22-Apr-2020 15:49:22 GMT; Max-Age=3600; Path=/'
    return resp

@app.route('/get_cookie')
def get_cookie():
    name = request.cookies.get('name','')
    city = request.cookies.get('city','')
    return name + city


@app.route('/delete_cookie')
def delete_cookie():
    resp = make_response("delete success")
    resp.delete_cookie("name")
    return resp

# ----------------------  session 机制 ---------------------------------

# from flask impoer session
# 设置session,需要设置秘钥字符串
# flask session需要的秘钥字符串
# flask 默认将session保存在cookie中
app.config['SECRET_KEY'] = 'cndsjkfncjkdsnvk165d45e4d0'
@app.route('/set_session')
def set_session():
    session['name'] = "assasinsteven"
    session['age'] = 235
    session['mobile'] = '18311039504'
    return 'set session success'

@app.route('/get_session')
def get_session():
    name = session.get('name')
    age = session.get('age')
    return 'get session success,name: %s,age:%s' %(name,age)


@app.route('/delete_session')
def delete_session():
    return "delete session success"

# ---------------- 请求钩子----------------------------------------------------

@app.route('/request')
def request():
    print('request page')
    return 'request success'

@app.before_first_request
def handle_before_first_request():
    # 在第一次请求处理之前先被执行
    print("handle_before_first_request 被执行 ")

@app.before_request
def handle_before_request():
    # 在每次请求之前都被执行
    print("handle_before_request 被执行")

@app.after_request
def handle_after_request(response):
    # 在每次请求(视图函数处理)之后都被执行,
    # 前提是视图函数没有出现异常
    print("handle_after_request 被执行")
    return response

@app.teardown_request
def handle_teardown_request(response):
    # 在每次请求(视图函数处理)之后都被执行,
    # 无论视图函数是否出现异常都被执行,工作在非调试模式时 debug=False
   # path = request.path
   # if path == url_for('request'):
   #     print("在请求钩子中判断请求的视图逻辑: request")
    print("handle_teardown_request 被执行")
    return response

#----------------------------------------------------------------------------
# g 变量 存储变量的容器
# from flask import g
@app.route('/g')
def g_var():
    g.username = "shibin"
    g.city = '北京'
    g.address = '北京昌平区'
    return 'g 变量'

def say_hello():
    username = g.username
    city = g.city
    pass


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
```

### 6.  hook

```python
from flask import Flask,request,\
    render_template,make_response,current_app,jsonify,session,url_for,g


app = Flask(__name__)

@app.route('/index')
def index():
    print('index 被执行')
	# age = 1 / 0
    return 'index page'


@app.before_first_request
def handle_before_first_request():
    """第一次请求处理之前先被执行"""
    print("handle_before_first_request 被执行 ")


@app.before_request
def hanlde_before_request():
    """每次请求之前都被执行"""
    print('hanlde_before_request被执行')

@app.after_request
def handle_after_request(response):
    # 在每次请求(视图函数处理)之后都被执行,
    # 前提是视图函数没有出现异常
    print("handle_after_request 被执行")
    return response

@app.teardown_request
def handle_teardown_request(response):
    # 在每次请求(视图函数处理)之后都被执行,
    # 无论视图函数是否出现异常都被执行,工作在非调试模式时 debug=False
   # path = request.path
   # if path == url_for('request'):
   #     print("在请求钩子中判断请求的视图逻辑: request")
    print("handle_teardown_request 被执行")
    return response


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
```

### 7. flask-script

```python
# pip install Flask-Script

from flask import Flask
from flask_script import Manager # 启动命令的管理类


app = Flask(__name__)

# 创建管理类对象
manager = Manager(app)

@app.route('/')
def index():
    return 'index page'

if __name__ == '__main__':
    # app.run('0.0.0.0',port=5001,debug=True)
    manager.run()
    # script.py runserver -h 0.0.0.0 -p 5001 --debug
```

### 8. filter

```python
from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def index():
    data = {
        "name" : "python",
         'age' : 18,
        "my_dict" : {
            "city":"beijing",
        },
        "list":[1,2,3,4,5],
        "int": 0
    }
    return render_template('index.html',**data)

# 自定义过滤器
# 1. 函数注册方式
def list_filter_step(list):
    return list[::2]
# 注册过滤器
app.add_template_filter(list_filter_step,'filter_list')

# 2. 装饰器方式
@app.template_filter('filter_list2')
def list_filter_step(list):
    return list[::3]

if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
```

### 9. WTF 

```python
# pip install Flask-WTF

# WTForms支持的HTML标准字段
# 字 段 对 象					说  明
# StringField				文本字段
# TextAreaField			多行文本字段
# PasswordField			密码文本字段
# HiddenField			隐藏文件字段
# DateField				文本字段，值为 datetime.date 文本格式
# DateTimeField			文本字段，值为 datetime.datetime 文本格式
# IntegerField			文本字段，值为整数
# DecimalField			文本字段，值为decimal.Decimal
# FloatField			文本字段，值为浮点数
# BooleanField			复选框，值为True 和 False
# RadioField				一组单选框
# SelectField				下拉列表
# SelectMutipleField		下拉列表，可选择多个值
# FileField				文件上传字段
# SubmitField				表单提交按钮
# FormField				把表单作为字段嵌入另一个表单
# FieldList				一组指定类型的字段

# WTForms常用验证函数
# 验证函数			说 明
# DataRequired		确保字段中有数据
# EqualTo			比较两个字段的值，常用于比较两次密码输入
# Length			验证输入的字符串长度
# NumberRange		验证输入的值在数字范围内
# URL					验证URL
# AnyOf				验证输入值在可选列表中
# NoneOf			验证输入值不在可选列表中

# 使用 Flask-WTF 需要配置参数 SECRET_KEY。
# CSRF_ENABLED是为了CSRF（跨站请求伪造）保护。 SECRET_KEY用来生成加密令牌，当CSRF激活的时候，该设置会根据设置的密匙生成加密令牌。

```

```python
from flask import Flask,render_template,request,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo


app = Flask(__name__)

app.config['SECRET_KEY'] = '199203522508s275hi72b782i278ns8272nw157ihd782eu'

# 定义表单模型类
class RegisterForm(FlaskForm):
    """自定义注册表单模型类"""
    #     名 称                                        验证器
    username = StringField(label=u'用户名',validators=[DataRequired(u'用户名不能为空')])
    password = PasswordField(label=u'密码',validators=[DataRequired(u'密码名不能为空')])
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired(u'密码名不能为空'),
                                                        EqualTo('password',u'两次输入密码不一致')])
    submit = SubmitField(label=u'提交注册')


@app.route('/')
def index():
    username = session.get("username"," ")
    return 'index page %s' % username



@app.route('/register',methods=['GET','POST'])
def login():
    # 创建form表单对象,如果是post请求,前段提交了数据
    # flask会把数据在构造form对象的时候,存放到对象中;无需判断请求方法
    form = RegisterForm()
    # 判断 form 表单数据 若数据满足所有的验证器 返回 true ;or false
    if form.validate_on_submit():
        # 验证通过
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('register.html',form = form)


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<form  method="post">
    {{ form.csrf_token }}
   <p>
        {{ form.username.label  }}
   </p>
    <p>
        {{ form.username }}
    </p>
{#    {{ form.username.errors }}#}
    {% for msg in form.username.errors %}
        <p> {{ msg }}</p>
    {% endfor %}

    <p>
        {{ form.password.label  }}
   </p>
    <p>
        {{ form.password }}
    </p>
{#    {{ form.username.errors }}#}
    {% for msg in form.password.errors %}
        <p> {{ msg }}</p>
    {% endfor %}

     <p>
        {{ form.password2.label  }}
     </p>
    <p>
        {{ form.password2 }}
    </p>
{#    {{ form.username.errors }}#}
    {% for msg in form.password2.errors %}
        <p> {{ msg }}</p>
    {% endfor %}

    {{ form.submit }}


{# 宏  #}
{% macro input() %}
    <input type="text" value="" size="30">
{% endmacro %}

<h1>第一次调用</h1>
{{ input() }}
<h1>第二次调用</h1>
{{ input() }}

    <hr />
<h1>定义带参数的宏</h1>
{% macro input2(type="text",value="",size=30) %}
    <input type="{{ type }}" value="{{ value }}" size="{{ size }}">
{% endmacro %}
<h1>带参数的宏</h1>
{{ input2('password','',15) }}
</form>
</body>
</html>
```

### 10.  SQLAlchemy

```python
# pip install flask-sqlalchemy
# pip install flask-mysqldb
```

```python
from flask import Flask,render_template,\
    request,redirect,url_for,session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,func
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)

#-------------------------------------------------------------
# database config paprams
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://user:user_pwd@host:port/db_name"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:19920308shibin@127.0.0.1:3306/flask_study"
# 设置每次请求结束后会自动提交数据库修改 不推荐使用
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# sqlalchemy自动跟踪数据库
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句 推荐使用
# app.config['SQLALCHEMY_ECHO'] = True
#-------------------------------------------------------------

# 使用类的方式配置
class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flask_study"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'index page '


# 创建数据库模型类
class Role(db.Model):
    """用户角色表"""
    __tablename__ = 'tbl_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),unique=True)

    users = db.relationship("User",backref='role')

    def __repr__(self):
        """定义后 可以让显示对象时更加直观"""
        return " Role object: name = %s" % self.name


class User(db.Model):
    """ user 数据表"""
    __tablename__ = 'tbl_users' # 指定数据表名称

    id = db.Column(db.Integer,primary_key=True) # 整型的主键,会默认为自增主键
    name = db.Column(db.String(64),unique=True)
    email = db.Column(db.String(128),unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('tbl_roles.id'))

    def __repr__(self):
        """定义后 可以让显示对象时更加直观"""
        return " User object: name = %s" % self.name




if __name__ == '__main__':
    # 清空数据库,
    db.drop_all()
    # 创建数据表
    db.create_all()

    role1 = Role(name='admin')
    db.session.add(role1)
    db.session.commit()


    role2 = Role(name='stuff')
    db.session.add(role2)
    db.session.commit()

    us1 = User(name='wang',email='wang@163.com',password='123456',role_id= role1.id)
    us2 = User(name='zhang',email='zhang@189.com',password='201504',role_id= role2.id)
    us3 = User(name='chen',email='chen@169.com',password='987456',role_id= role2.id)
    us4 = User(name='zhao',email='zhao@163.com',password='323245978',role_id= role1.id)

    db.session.add_all([us1,us2,us3,us4]) #批量写入
    db.session.commit()

    # 查询操作
    # Role.query.all()  # 查询全部
    # Role.query.first()  # 查询一条 第一条记录
    # Role.query.get(主键)  # 查询一条 只接受主键值

    # db.session.query(Role).all() # db 查询

    # User.query.filter_by(User.name='wang',User.role_id=1).first() # 过滤查询 and
    # User.query.filter=(User.name=='wang',User.role_id==1).first() # 过滤查询 and
    # or_ 关系
    # User.query.filter=(or_(User.name=='wang',User.email.endswith('163.com'))).first() # 过滤查询 or
    # limit
    # User.query.filter().offset().limit().order_by(User.id.desc()).all()
    # order_by
    # User.query.filter().order_by(User.id.asc()).all()
    # group_by  from sqlalchemy import func
    # users = db.session.query(User.role_id,func.count(User.role_id)).group_by(User.role_id).all()

    # update 先查询,后保存
    # user = User.query.first()
    # user.name = 'shibin'
    # db.session.add(user)
    # db.session.commit()

    # 查询时更新
    # User.query.filter_by(name='zhou').update({"name":"assasin","email":"assasin@163.com"})
    # db.session.commit()

    # delete
    # user = User.query.get(3)
    # db.session.delete(user)
    # db.session.commit()
    
    
    
    app.run('0.0.0.0',port=5001,debug=True)

```

### 11. Migrate

```python
# pip install flask-migrate
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand

# python migration.py db init  # 初始化
# python migration.py db migrate # 生成迁移
# python migration.py db migrate -m '备注信息' # 生成迁移
# python migration.py db upgrade # 修改后升级
# python migration.py db history # 查看历史记录
# python migration.py db downgrade 6d53c7ca7544 # 回退至某个历史版本
```

```python
from flask import Flask,render_template,request,redirect,Response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand
from sqlalchemy import or_,func

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
manager = Manager(app)

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flask_study"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

app.config.from_object(Config)
db = SQLAlchemy(app)
# 第一个参数是flask实例,第二个参数是sqlalchemy数据库参数
migrate = Migrate(app,db)
# manager是flask-script实例,在flask-script中添加一个db命令
manager.add_command('db',MigrateCommand)

class Author(db.Model):
    """author"""
    __tablename__ = 'tbl_authors'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)
    books = db.relationship('Book',backref='author')

class Book(db.Model):
    """books"""
    __tablename__ = 'tbl_books'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    author_id = db.Column(db.Integer,db.ForeignKey('tbl_authors.id'))



if __name__ == '__main__':
    # app.run('0.0.0.0',port=5001,debug=True)
    manager.run()
```

### 12. flask-mail

```python
# pip install flask-mail
from flask_mail import Mail,Message
app = Flask(__name__)
# 一次性配置多条
app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.sina.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS= True,
    MAIL_USERNAME =  'assasin@sina.com',
    MAIL_PASSWORD =  '*******',

)
```

```python
from flask import Flask,render_template,request,redirect,Response
from flask_mail import Mail,Message


app = Flask(__name__)
# 一次性配置多条
app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.sina.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS= True,
    MAIL_USERNAME =  'assasin@sina.com',
    MAIL_PASSWORD =  '*******', # 密码 / 授权码
)
mail = Mail(app)

@app.route('/')
def index():
    # sender 发送方 ; recipients 接收方
    msg = Message("this is a test",sender='assasin@sina.com',recipients=['8392@qq.com'])
    # 邮件内容
    msg.body = "flask is best"
    # 发送
    mail.send(msg)
    print("send success")
    return 'index page '


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001)
```

### 13.  Blueprint 

```python
# main.py

from flask import Flask
from orders import app_orders



app = Flask(__name__)

# 注册蓝图
app.register_blueprint(app_orders)
app.register_blueprint(app_orders,url_prefix='/orders') # 添加路由前缀

@app.route('/')
def index():

    return 'index page '



if __name__ == '__main__':
    print(app.url_map)
    app.run('0.0.0.0',port=5001,debug=True)
```

```python
# order.py

from flask import Blueprint

# 创建蓝图对象 蓝图就是一个小模块的抽象概念
app_orders = Blueprint("app_orders",__name__)

@app_orders.route('/get_orders')
def get_orders():
    return 'get_orders page '
```

```json
├─blue
│  --- main.py
|  --- goods.py
|  --- users.py
|  --- orders.py
├─cart
│  ├─static
│  ├─templates
│  --- __init__.py
│  --- views.py

......详见上边 
```

### 14.  unit test

```python
# login.py

from flask import Flask,request,jsonify



app = Flask(__name__)

@app.route('/login',methods=['POST'])
def login():
   user_name = request.form.get('user_name')
   password = request.form.get('password')

   if not all([user_name,password]):
       resp = {
           "errcode": 1,
           'errmsg': '参数不完整',
           'data': ''
       }
       return jsonify(resp)

   if user_name == 'admin' and password == 'python':
        resp = {
            "errcode": 0,
            "errmsg": 'login success',
            'data': ''
        }
        return jsonify(resp)
   else:
       resp = {
           "errcode": 2,
           "errmsg": 'user_name error',
           'data': ''
       }
       return jsonify(resp)



if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
```

```python
# test.py

import unittest
from login import app
import json


class LoginTest(unittest.TestCase):
    """构造单元测试案例"""
    def test_empty_username_password(self):
        """测试用户名与密码不完整的情况"""
        # 创建进行web请求的客户端,使用flask提供的
        client = app.test_client()
        #利用客户端模拟发送请求
        ret = client.post('/login',data={}) # 模拟发送
        # ret 是视图返回的响应对象,data属性是响应体的数据
        resp = ret.data
        resp = json.loads(resp)

        # 断言测试
        self.assertIn('errcode',resp)
        self.assertEqual(resp['errcode'],1)


if __name__ == '__main__':
    unittest.main()

```

### 15.   

```python

```

### 16.  

```python

```

### 17.  

```python

```

### 18.  

```python

```

### 19.  

```python

```

### 20.   flask + gunicorn + nginx

```shell
# pip install gunicore
 gunicorn -w 4 -b 127.0.0.1:5000 -D --access-logfile ./logs/log  main:app
 gunicorn -w 4 -b 127.0.0.1:5001 -D --access-logfile ./logs/log  main:app
# -w n 开启n个进程 worker
# -b 127.0.0.0:5000 绑定至哪个服务器
# -D 以后台守护进程方式运行
#  --access-logfile DIR/FILE 日志文件存储路径
# main:app  main.py的app对象

 # 配置 nginx负载均衡
 upstram flask {
     server 127.0.0.1:5000;
     server 127.0.0.1:5001;
 }
 server {
     listen      80;
     server_name  localhost;

     location / {
         proxy_pass http://flask;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
     }
 }

 # restart nginx server
 usr/local/sbin/nginx -s reload
```

### 21.  

```python

```

### 22.  

```python

```

### 23.  

```python

```

### 24.  

```python

```

### 25.   

```python

```

### 26.  

```python

```

### 27.  

```python

```

### 28.  

```python

```

### 29. 

```python

```

### 30.  

```python

```

### 31.  

```python

```

### 32. 

```python

```

### 33. 

```python

```

### 34. 

```python

```

### 35.  

```python

```

### 36. 

```python

```

### 37. 

```python

```

### 38. 

```python

```

### 39. 

```python

```

