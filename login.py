from flask import Flask,request,jsonify



app = Flask(__name__)

@app.route('/login',methods=['POST'])
def login():
   user_name = request.form.get('user_name')
   password = request.form.get('password')

   if not all([user_name,password]):
       resp = {
           "errcode": 1,
           'errmsg': '参数不完整',
           'data': ''
       }
       return jsonify(resp)

   if user_name == 'admin' and password == 'python':
        resp = {
            "errcode": 0,
            "errmsg": 'login success',
            'data': ''
        }
        return jsonify(resp)
   else:
       resp = {
           "errcode": 2,
           "errmsg": 'user_name error',
           'data': ''
       }
       return jsonify(resp)



if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)