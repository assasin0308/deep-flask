from flask import Flask
from goods import goods
from users import register
from orders import app_orders
from cart import app_cart
# 循环引用问题,推迟一方导入,先让另一方导入


app = Flask(__name__)
app.route('/goods')(goods)
app.route('/register')(register)

# 注册蓝图
app.register_blueprint(app_orders,url_prefix='/orders')
app.register_blueprint(app_cart,url_prefix='/cart')

@app.route('/')
def index():
    return 'index page '



if __name__ == '__main__':
    print(app.url_map)
    app.run('0.0.0.0',port=5001,debug=True)