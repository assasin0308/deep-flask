from flask import Blueprint

# 创建蓝图对象 蓝图就是一个小模块的抽象概念
app_orders = Blueprint("app_orders",__name__)

@app_orders.route('/get_orders')
def get_orders():
    return 'get_orders page '

@app_orders.route('/post_orders')
def post_orders():
    return 'post_orders page '