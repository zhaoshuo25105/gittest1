
import random, time

# source = [ random.randrange(10000+i) for i in range(10000)]


# step = int(len(source)/2) #分组步长
# print(step)
# t_start = time.time()


# def shell_sort(lists):
#     # 希尔排序
#     count = len(lists)
#     step = 2
#     group = int(count // 2)
#     while group > 0:
#         for i in range(0, group):
#             j = i + group
#             while j < count:
#                 k = j - group
#                 key = lists[j]
#                 while k >= 0:
#                     if lists[k] > key:
#                         lists[k + group] = lists[k]
#                         lists[k] = key
#                     k -= group
#                 j += group
#         group /= step
#     return lists

# if __name__ == "__main__":
#     source = [8, 6, 4, 9, 7, 3, 2, -4, 0, -100, 99]
#     print(source)
#     s = shell_sort(source)
#     print(s)




# def shell_sort(alist):
#     """希尔排序"""
#     n = len(alist)
#     # 步长
#     gap = n // 2
   
#     while gap >= 1:
#         #j代表后段
#         for j in range(gap, n):
#             # i = j
#             #代表前段
#             while (j - gap) >= 0:
#                 #后段和前段比较大小
#                 if alist[j] < alist[j - gap]:
#                     alist[j], alist[j - gap] = alist[j - gap], alist[j]
#                     #从新判断交换完数据的大小
#                     j -= gap
#                 else:
#                     break
#         print(alist)
#         gap //= 2


# if __name__ == '__main__':
#     alist = [54, 26, 93, 17, 77, 31, 44, 55, 20]
#     print("原列表为：%s" % alist)
#     shell_sort(alist)
#     print("新列表为：%s" % alist)



l=[1,2,3]
def f(n=0,lst=[]):
    lst.append(n)
    print(lst)

f(4,l)
f(5,l)
f(100)
f(200)


# 修改可变变量
# a = [3,4]
# def func():
#     a.append(5)
#     print(a)
# func()
# a.append(6)
# print(a)


# l = ['hello','word']
# print('＃'.join(l))

# str1='asdfg'
# print(str1.split('g'))

class Game():
    @staticmethod
    def menu():
        print('开始请按１')
game = Game()
Game.menu()


s1 = '1+2*3'
v = eval(s1)
print(v)

def make_power(y):
    def fn(x):
        return x**y
    return fn
pow2 = make_power(2)
print(pow2(3))