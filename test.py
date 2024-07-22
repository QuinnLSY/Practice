# print("hello python")
# 循环输出
# for i in range(1,10):
#     print(i,end=" ")

# 条件语句
# while(1):
#     m=int(input())
#     if m>=0 and m<60:
#         print("不及格")
#     else:
#         print("及格")

# 两数之和
# n1=eval(input("请输入第一个数字："))#eval:评估函数，将input的字符型数据转换为int或float
# n2=eval(input("请输入第二个数字："))
# sum=n1+n2
# print("两数之和为：",sum)

#求数的阶乘
# count=1
# for i in range(1,6):
#     count*=i
# print(count)

# 求区间内的所有素数
# def total_prime(n,m):
#     result=[]
#     if n>m:
#         return False
#     if n<=0:
#         return False
#     for i in range(n,m+1):
#         if is_prime(i)==True:
#             result.append(i)
#     return result
#
# def is_prime(n):
#     if n<1:
#         return False
#     for i in range(2,n):
#         if n%i==0:
#             return False
#     return True
# n=int(input("请输入左区间："))
# m=int(input("请输入右区间："))
# print(total_prime(n,m))

#计算圆的面积
# import math
# r=eval(input("请输入圆的半径："))
# area=math.pi*r*r
# area=math.pi*r**2
# print("圆的面积是：",area)

# 计算列表数字的和
# li=[2,4,7]
# def sum(li):
#     total=0
#     for i in li:
#          total+=i
#     return total
# print("列表数字和为：%s"%sum(li)) #字符串格式化输出
# print(sum(li)) #内置求和函数一键求和

# 范围内所有偶数
# def num(n1,n2):
#     result=[]
#     for i in range(n1,n2+1):
#         if i%2==0:
#             result.append(i)
#     return result
# n1=eval(input("输入右区间："))
# n2=eval(input("输入左区间："))
# print("%d到%d区间范围内的偶数有："%(n1,n2),num(n1,n2)) #字符串格式化即c语言中输出变量时的%d，但python中被输出值也要加%

# 列表去重
# li=[10,20,30,20,10]
# # print(set(li))#转换成集合
# qli=[]
# for i in li:
#     if i not in qli: #直接判断不在
#         qli.append(i)
# print(qli)

# 列表排序
# li=[3,5,17,9,13]
# li.sort()
# print(li)
# sli=sorted(li)
# print(sli)
# rsli=sorted(li,reverse=True)#降序排列
# print(rsli)

