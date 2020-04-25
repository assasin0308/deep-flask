from flask import Flask,render_template,request,redirect,Response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand
from sqlalchemy import or_,func

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
manager = Manager(app)

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:19920308shibin@127.0.0.1:3306/flask_study"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

app.config.from_object(Config)
db = SQLAlchemy(app)
# 第一个参数是flask实例,第二个参数是sqlalchemy数据库参数
migrate = Migrate(app,db)
# manager是flask-script实例,在flask-script中添加一个db命令
manager.add_command('db',MigrateCommand)

class Author(db.Model):
    """author"""
    __tablename__ = 'tbl_authors'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)
    books = db.relationship('Book',backref='author')

class Book(db.Model):
    """books"""
    __tablename__ = 'tbl_books'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    author_id = db.Column(db.Integer,db.ForeignKey('tbl_authors.id'))



if __name__ == '__main__':
    # app.run('0.0.0.0',port=5001,debug=True)
    manager.run()