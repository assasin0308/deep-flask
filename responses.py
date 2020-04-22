from flask import Flask,request,\
    render_template,make_response,current_app
import json


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


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)