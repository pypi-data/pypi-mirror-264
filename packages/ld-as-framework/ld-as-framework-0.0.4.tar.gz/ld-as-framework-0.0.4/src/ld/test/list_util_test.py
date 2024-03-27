if __name__ == 'ld.test.list_util_test':
    from ..common.ListUtil import ListUtil, 列表
    list = ['123', 4, '测试']
    list = ['sad ', 'as', 't', 'as']
    print(ListUtil.get_len(list))
    print(列表.获取长度(list))
    print(ListUtil.judgement_empty(list))
    print(列表.是否为空(list))
    print(ListUtil.sort_forward(list))
    print(列表.正向排序(list))
    print(ListUtil.sort_reverse(list))
    print(列表.反向排序(list))
    print(ListUtil.sort_random(list))
    print(列表.随机排序(list))
    print(ListUtil.remove_duplicates(list))
    print(列表.删除重复(list))