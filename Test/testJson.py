def check_type(num):
    # 获取参数的类型
    data_type = type(num)

    if data_type == int:
        # 参数是int类型
        print("参数类型为int")
    elif data_type == float:
        # 参数是float类型
        print("参数类型为float")
    else:
        # 参数类型不为int或float
        print("参数类型不为int或float")
if __name__ == '__main__':
    a = 1
    b = 1
    c = a+b
    print(c)

    f = 2*a*b/(a+b+1e-10)
    print(f)

    check_type(a)  # 参数类型为int
    check_type(a+b)  # 参数类型为float
    check_type(a+b+1e-10)
    check_type(f)

