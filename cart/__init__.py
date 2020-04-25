from flask import Blueprint

# 创建蓝图
app_cart = Blueprint("app_cart",__name__,template_folder='templates')

# 在__init__文件被执行时候  把视图加载进来,让蓝图与应用程序知道 有视图的存在

from .views import  get_cart
