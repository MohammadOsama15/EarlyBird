list1 = [x for x in range(0, 5)]
list2 = [x for x in range(1, 6)]


def func_1(arg1: list, arg2: list):
    zipped = zip(arg1, arg2)
    return (zipped)


def func_2(arg1: list, arg2: list):
    zipped = zip(arg1, arg2)
    list(zipped)
    return (zipped)


print("function 1 returns: ")
for i, j in func_1(list1, list2):
    print(i, j)
print("function 2 returns: ")
for i, j in func_2(list1, list2):
    print(i, j)
