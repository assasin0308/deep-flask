# coding:utf-8
from flask import Flask,request,render_template,make_response

app = Flask(
    __name__,
    static_url_path='/python', # 访问静态资源的url前缀,默认 static
    static_folder='jingtai', # 静态文件存放目录,默认 static
    template_folder='muban', # 模板文件目录 ,默认 templates
)   # 同 app = Flask('__main__')




@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

