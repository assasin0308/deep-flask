import unittest
from login import app
import json


class LoginTest(unittest.TestCase):
    """构造单元测试案例"""
    def setUp(self):
        """在进行测试之前先被执行"""
        # 设置flask工作在测试模式下
        # app.config['TESTING'] = True
        # app.testing = True
        self.client = app.test_client()

    def test_empty_username_password(self):
        """测试用户名与密码不完整的情况"""
        # 创建进行web请求的客户端,使用flask提供的
        # client = app.test_client()
        #利用客户端模拟发送请求
        ret = self.client.post('/login',data={}) # 模拟发送
        # ret 是视图返回的响应对象,data属性是响应体的数据
        resp = ret.data
        resp = json.loads(resp)

        # 断言测试
        self.assertIn('errcode',resp)
        self.assertEqual(resp['errcode'],1)


    def test_wrong_user_passwd(self):
        """测试错误的用户名与密码"""
        # client = app.test_client()
        # 利用客户端模拟发送请求
        ret = self.client.post('/login', data={
            "user_name":"admin",
            "password":"python"
        })  # 模拟发送
        # ret 是视图返回的响应对象,data属性是响应体的数据
        resp = ret.data
        resp = json.loads(resp)
        # 断言测试
        self.assertIn('errcode', resp)
        self.assertEqual(resp['errcode'], 0)





if __name__ == '__main__':
    unittest.main()
