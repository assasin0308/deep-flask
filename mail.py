from flask import Flask,render_template,request,redirect,Response
from flask_mail import Mail,Message


app = Flask(__name__)
# 一次性配置多条
app.config.update(
    DEBUG = True,
    MAIL_SERVER = 'smtp.sina.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS= True,
    MAIL_USERNAME =  'assasin0308@sina.com',
    MAIL_PASSWORD =  '19920308shibin', # 密码 / 授权码
)
mail = Mail(app)

@app.route('/')
def index():
    # sender 发送方 ; recipients 接收方
    msg = Message("this is a test",sender='assasin0308@sina.com',recipients=['839203143@qq.com'])
    # 邮件内容
    msg.body = "flask is best"
    # 发送
    mail.send(msg)
    print("send success")
    return 'index page '


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001)