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
#



@app.route('/')
def index():
    # 读取配置参数
    # 1. 直接从全局对象app的config字典中取值
    # app.config["DEBUg"]
    # app.config.get("NAME")
    # 2. 通过current_app获取
    # print(current_app.config.get('NAME'))
    return 'hello world'

if __name__ == '__main__':
    # app.run() 参数配置:
    # host: '0.0.0.0' 默认 127.0.0.1
    # port: 5001 默认 5000
    # debug: True/False 开启/关闭debug模式
    # print(app.url_map) # 查看所有路由信息
    app.run(host='0.0.0.0',debug=True)


```

### 4. 

```python

```

### 5.  

```python

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

### 20.   

```python

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

