


def num_div(num1,num2):
    # assert 断言 表达式->true,则断言成功,程序继续执行,
    # 否则断言失败,抛出异常AssertionError,程序终止
    assert isinstance(num1,int)
    assert isinstance(num2,int)
    assert num2 != 0
    print(num1 / num2)



if __name__ == '__main__':
    num_div(200,500)