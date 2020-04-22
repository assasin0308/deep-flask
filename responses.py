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