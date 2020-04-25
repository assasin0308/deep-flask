import unittest
from login import app
import json


class LoginTest(unittest.TestCase):
    """构造单元测试案例"""
    def test_empty_username_password(self):
        """测试用户名与密码不完整的情况"""
        # 创建进行web请求的客户端,使用flask提供的
        client = app.test_client()
        #利用客户端模拟发送请求
        ret = client.post('/login',data={}) # 模拟发送
        # ret 是视图返回的响应对象,data属性是响应体的数据
        resp = ret.data
        resp = json.loads(resp)

        # 断言测试
        self.assertIn('errcode',resp)
        self.assertEqual(resp['errcode'],1)


if __name__ == '__main__':
    unittest.main()
