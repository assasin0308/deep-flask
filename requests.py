from flask import Flask,request,\
    render_template,make_response,current_app,abort,Response


app = Flask(__name__)

# request 常用属性说明
#---------------------------------------------------------------------------------
#        属 性              说 明                            类 型
#        data       记录请求的数据,并转化为字符串              *
#        form       记录请求中的表单数据                    MultiDict
#        args       记录请求中的查询参数                    MultiDict
#        cookies    记录请求中的cookie信息                  Dict
#        headers    记录请求中的报文头                      EnvironHeaders
#        method     记录请求使用的HTTP方法                  GET/POST
#        url        记录请求的url地址                       String
#        files      记录请求上传的文件                        *
#---------------------------------------------------------------------------------


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