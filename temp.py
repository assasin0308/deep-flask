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