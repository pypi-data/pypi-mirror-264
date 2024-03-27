if __name__ == 'ld.test.type_util_test':
    from ..common.TypeUtil import TypeUtil, 类型
    a = 123
    b = 123.456
    c = '零动学院'
    d = ['1', 2, 3]
    e = {'1': 1, '2': 2}
    f = True
    print(类型.判断类型(a))
    print(类型.是否列表(d))
    print(类型.是否字典(e))
    print(类型.是否布尔(f))
    print(类型.是否字符(c))
    print(类型.是否小数(b))
    print(类型.是否整数(a))
    print(类型.是否数字(b))
    print('11')