from flask import Flask,render_template,\
    request,redirect,url_for,session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,func
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)

#-------------------------------------------------------------
# database config paprams
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://user:user_pwd@host:port/db_name"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:19920308shibin@127.0.0.1:3306/flask_study"
# 设置每次请求结束后会自动提交数据库修改 不推荐使用
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# sqlalchemy自动跟踪数据库
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句 推荐使用
# app.config['SQLALCHEMY_ECHO'] = True
#-------------------------------------------------------------

# 使用类的方式配置
class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:19920308shibin@127.0.0.1:3306/flask_study"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'index page '


# 创建数据库模型类
class Role(db.Model):
    """用户角色表"""
    __tablename__ = 'tbl_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),unique=True)

    users = db.relationship("User",backref='role')

    def __repr__(self):
        """定义后 可以让显示对象时更加直观"""
        return " Role object: name = %s" % self.name


class User(db.Model):
    """ user 数据表"""
    __tablename__ = 'tbl_users' # 指定数据表名称

    id = db.Column(db.Integer,primary_key=True) # 整型的主键,会默认为自增主键
    name = db.Column(db.String(64),unique=True)
    email = db.Column(db.String(128),unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('tbl_roles.id'))

    def __repr__(self):
        """定义后 可以让显示对象时更加直观"""
        return " User object: name = %s" % self.name




if __name__ == '__main__':
    # 清空数据库,
    db.drop_all()
    # 创建数据表
    db.create_all()

    role1 = Role(name='admin')
    db.session.add(role1)
    db.session.commit()


    role2 = Role(name='stuff')
    db.session.add(role2)
    db.session.commit()

    us1 = User(name='wang',email='wang@163.com',password='123456',role_id= role1.id)
    us2 = User(name='zhang',email='zhang@189.com',password='201504',role_id= role2.id)
    us3 = User(name='chen',email='chen@169.com',password='987456',role_id= role2.id)
    us4 = User(name='zhao',email='zhao@163.com',password='323245978',role_id= role1.id)

    db.session.add_all([us1,us2,us3,us4]) #批量写入
    db.session.commit()

    # 查询操作
    # Role.query.all()  # 查询全部
    # Role.query.first()  # 查询一条 第一条记录
    # Role.query.get(主键)  # 查询一条 只接受主键值

    # db.session.query(Role).all() # db 查询

    # User.query.filter_by(User.name='wang',User.role_id=1).first() # 过滤查询 and
    # User.query.filter=(User.name=='wang',User.role_id==1).first() # 过滤查询 and
    # or_ 关系
    # User.query.filter=(or_(User.name=='wang',User.email.endswith('163.com'))).first() # 过滤查询 or
    # limit
    # User.query.filter().offset().limit().order_by(User.id.desc()).all()
    # order_by
    # User.query.filter().order_by(User.id.asc()).all()
    # group_by  from sqlalchemy import func
    # users = db.session.query(User.role_id,func.count(User.role_id)).group_by(User.role_id).all()

    # update 先查询,后保存
    # user = User.query.first()
    # user.name = 'shibin'
    # db.session.add(user)
    # db.session.commit()

    # 查询时更新
    # User.query.filter_by(name='zhou').update({"name":"assasin","email":"assasin@163.com"})
    # db.session.commit()

    # delete
    # user = User.query.get(3)
    # db.session.delete(user)
    # db.session.commit()
    


    # app.run('0.0.0.0',port=5001,debug=True)


