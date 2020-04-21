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

#------------- 自定义路由转换器 ----------------------

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

