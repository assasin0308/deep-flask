from flask import Flask,render_template,\
    request,redirect,url_for,session

app = Flask(__name__)

@app.route('/')
def index():
    return 'index page '


if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)