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

```

### 11. 

```python

```

### 12. 

```python

```

### 13.  

```python

```

### 14.  

```python

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

