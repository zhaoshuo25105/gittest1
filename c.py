


#
# n = int(input('请输入高度:'))
# a = ' '
# b = '*'
# for i in range(1,n+1):
#     c = (n - i)*a
#
#     d = (2*i-1)*b
#     print(c,d)
#
# for x in range(n):
#     print((n-1)*' ','*')


def outer(func):
    def inner():
        print("认证成功")
        result = func()
        print("添加日志成功")
        # return result
    return inner

# f1 = outer(f1)

@outer
def f1():
    print("业务部门１数据接口.........")
    # return 2

f1()
# res = f1()

# print(res)

# a = "a"
# print(a>"b" or "c")

# l = [1,2,3,4,5]
# b= l.reverse()
# a =list(reversed(l))
# print(a,b,l)






