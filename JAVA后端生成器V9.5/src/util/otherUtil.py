def permutation_and_combination(*args):
    start = 0
    max_size = 3
    if len(args) == 1:
        max_size = args[0]
    if len(args) == 2:
        start, max_size = args
    lists = []
    max_lists = []
    for i in range(start, max_size):
        # 滑块，最大该位最大滑块初始化
        lists_size = i + 1
        lists.clear()
        max_lists.clear()
        for j in range(lists_size):
            lists.append(j + 1)
        for j in range(lists_size):
            max_lists.append(max_size - j)
        max_lists.reverse()
        yield lists
        # 滑动
        while True:
            lists[-1] += 1
            for j in range(-1, 0 - lists_size, -1):
                if lists[j] > max_lists[j]:
                    lists[j] = lists[j - 1]
                    lists[j - 1] = lists[j - 1] + 1
            for j in range(lists_size - 1):
                if lists[j] > lists[j + 1]:
                    lists[j + 1] = lists[j] + 1

            if lists[0] > max_lists[0]:
                break
            else:
                yield lists
