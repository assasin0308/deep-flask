# deep-flask 

##### --version=0.10.1 

#### python2

##### flask + gunicorn + nginx

### 1. installation

```python
pip install flask

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

### 5.  response & cookie & session

```python
from flask import Flask,request,\
    render_template,make_response,current_app,jsonify,session


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
app.config['SECRET_KEY'] = 'cndsjkfncjkdsnvk165d45e4d0'
@app.route('/set_session')
def set_session():
    session['name'] = "assasinsteven"
    session['age'] = 235
    session['mobile'] = '18311039502 '
    return 'set session success'

@app.route('/get_session')
def get_session():
    name = session.get('name')
    age = session.get('age')
    return 'get session success,name: %s,age:%s' %(name,age)


@app.route('/delete_session')
def delete_session():
    """"""
    return "delete session success"



if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)
```

### 6.  

```python

```

### 7. 

```python

```

### 8. 

```python

```

### 9. 

```python

```

### 10.  

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

