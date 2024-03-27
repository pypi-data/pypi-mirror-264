if __name__ == 'ld.test.time_util_test':
    from ..common.TimeUtil import TimeUtil, 时间
    import time
    print(时间.获取当前时间戳())
    s1 = 时间.获取当前时间戳()
    time.sleep(3)
    s2 = 时间.获取当前时间戳()
    print(时间.时间差(s1, s2))