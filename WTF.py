from flask import Flask,render_template,request,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo


app = Flask(__name__)

app.config['SECRET_KEY'] = '199203522508s275hi72b782i278ns8272nw157ihd782eu'

# 定义表单模型类
class RegisterForm(FlaskForm):
    """自定义注册表单模型类"""
    #     名 称                                        验证器
    username = StringField(label=u'用户名',validators=[DataRequired(u'用户名不能为空')])
    password = PasswordField(label=u'密码',validators=[DataRequired(u'密码名不能为空')])
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired(u'密码名不能为空'),
                                                        EqualTo('password',u'两次输入密码不一致')])
    submit = SubmitField(label=u'提交注册')


@app.route('/')
def index():
    username = session.get("username"," ")
    return 'index page %s' % username



@app.route('/register',methods=['GET','POST'])
def login():
    # 创建form表单对象,如果是post请求,前段提交了数据
    # flask会把数据在构造form对象的时候,存放到对象中;无需判断请求方法
    form = RegisterForm()
    # 判断 form 表单数据 若数据满足所有的验证器 返回 true ;or false
    if form.validate_on_submit():
        # 验证通过
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('register.html',form = form)


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)