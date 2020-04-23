from flask import Flask
from flask_script import Manager # 启动命令的管理类


app = Flask(__name__)

# 创建管理类对象
manager = Manager(app)

@app.route('/')
def index():
    return 'index page'

if __name__ == '__main__':
    # app.run('0.0.0.0',port=5001,debug=True)
    manager.run()
    # script.py runserver -h 0.0.0.0 -p 5001 --debug