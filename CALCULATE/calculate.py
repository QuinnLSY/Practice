# -*- coding:utf-8 -*-
"""
:author: 单纯同学
:time: 2023-08-03
:software: pycharm
"""
import tkinter as tk
from tkmacosx import Button

font_20 = ('宋体', 20)
font_16 = ('宋体', 16)
bw = 66
br = 40

root = tk.Tk()
root.title('简易计算器')
root.geometry('296x330+620+300')  # 窗口大小(横x竖)+横向显示位置+纵向显示位置
root.attributes("-alpha", 0.9)  # 不透明度
# root["background"] = "#ffffff"  # 背景颜色

# 数字显示屏
last = tk.StringVar()  # 上一次结果
last.set('last result: 0')
result_num = tk.StringVar()  # 本次结果
result_num.set(0)
tk.Label(root,
         textvariable=last, font=font_20, height=1, width=22,
         justify=tk.LEFT, anchor=tk.SE, bg='#ffffff', relief=tk.SUNKEN  # 左对齐，固定点：右下角,背景颜色
         ).grid(row=1, column=1, columnspan=4)
tk.Label(root,
         textvariable=result_num, font=font_20, height=1, width=22,
         justify=tk.LEFT, anchor=tk.SE, bg='#ffffff', relief=tk.SUNKEN  # 左对齐，固定点：右下角，背景颜色
         ).grid(row=2, column=1, columnspan=4)
# 显示监测到的按键
txt = tk.StringVar()
txt.set('按键检测')
tk.Label(root,
         textvariable=txt, font=font_16, height=2, width=28,
         justify=tk.CENTER, anchor=tk.CENTER, bg='#ffffff'  # 左对齐，固定点：右下角,背景颜色
         ).grid(row=8, column=1, rowspan=2, columnspan=4)

# 功能及数字按钮
# 第一行：清除 回退 除 乘
button_clear = Button(root, text='C', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#b1b2b2')
button_back = Button(root, text='⌫', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#b1b2b2')
button_division = Button(root, text='/', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#b1b2b2')
button_multiply = Button(root, text='*', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#b1b2b2')
button_clear.grid(row=3, column=1, padx=4, pady=2)  # 几行，几列，横向间距，纵向间距
button_back.grid(row=3, column=2, padx=4, pady=2)
button_division.grid(row=3, column=3, padx=4, pady=2)
button_multiply.grid(row=3, column=4, padx=4, pady=2)

# 第二行：7 8 9 减
button_seven = Button(root, text='7', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_eight = Button(root, text='8', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_nine = Button(root, text='9', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_subtraction = Button(root, text='—', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#b1b2b2')
button_seven.grid(row=4, column=1, padx=4, pady=2)  # 几行，几列，横向间距，纵向间距
button_eight.grid(row=4, column=2, padx=4, pady=2)
button_nine.grid(row=4, column=3, padx=4, pady=2)
button_subtraction.grid(row=4, column=4, padx=4, pady=2)

# 第三行：4 5 6 加
button_four = Button(root, text='4', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_five = Button(root, text='5', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_six = Button(root, text='6', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_plus = Button(root, text='+', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#b1b2b2')
button_four.grid(row=5, column=1, padx=4, pady=2)  # 几行，几列，横向间距，纵向间距
button_five.grid(row=5, column=2, padx=4, pady=2)
button_six.grid(row=5, column=3, padx=4, pady=2)
button_plus.grid(row=5, column=4, padx=4, pady=2)

# 第四行：1 2 3 =
button_one = Button(root, text='1', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_two = Button(root, text='2', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_three = Button(root, text='3', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_equal = Button(root, text='=', width=bw, height=2 * br + 5, font=font_16, relief=tk.FLAT, bg='#b1b2b2')
button_one.grid(row=6, column=1, padx=4, pady=2)  # 几行，几列，横向间距，纵向间距
button_two.grid(row=6, column=2, padx=4, pady=2)
button_three.grid(row=6, column=3, padx=4, pady=2)
button_equal.grid(row=6, column=4, padx=4, pady=2, rowspan=2)  # 几行，几列，横向间距，纵向间距,行占用

# 第5行：0 0 . =
button_zero = Button(root, text='0', width=2 * bw + 7, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_dot = Button(root, text='.', width=bw, height=br, font=font_16, relief=tk.FLAT, bg='#eacda1')
button_zero.grid(row=7, column=1, padx=4, pady=2, columnspan=2)  # 几行，几列，横向间距，纵向间距，列占用
button_dot.grid(row=7, column=3, padx=4, pady=2)

"""鼠标点击事件"""

result_set = ['0']  # 存储上一次结果，用于在第一行显示
button_set = []  # 每一步公式的存储数组，用于返回按钮


# 处理按钮功能
def click_button(x):
    # last.set('last result:'+result_set[0])
    button_set.append(result_num.get())  # 加入上一步的公式
    if result_num.get() == '0':  # 初始值为0，第一次输入时应不显示这个0
        result_num.set(x)
    else:
        if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(button_set) == 1:
            button_set.pop()
            return
        result_num.set(result_num.get() + x)


# 计算，button_calculate的用法
def calculate():
    formula = result_num.get()
    result = eval(formula)  # eval自动计算
    if result % 1 == 0:  # 除法时默认结果为float类型，若为整数，应转换为int类型
        result = int(result)
    result_num.set(str(result))  # 显示结果
    last.set('last result: ' + result_set.pop())  # 第一行显示上一次结果，方便观察
    # result_set.pop()
    result_set.append(str(result))  # 加入本次结果
    button_set.clear()  # 清除本次计算的公式，因为得到结果后，不允许back


# 清除，button_clear的用法
def clear():
    result_num.set(0)
    last.set('last result: ' + result_set.pop())  # 清除本次结果，在上次结果中显示


# 返回，button_back的用法
def back():
    if len(button_set) == 0:
        return
    result_num.set(button_set.pop())


# 唤起对应按钮功能
button_one.config(command=lambda: click_button('1'))
button_two.config(command=lambda: click_button('2'))
button_three.config(command=lambda: click_button('3'))
button_four.config(command=lambda: click_button('4'))
button_five.config(command=lambda: click_button('5'))
button_six.config(command=lambda: click_button('6'))
button_seven.config(command=lambda: click_button('7'))
button_eight.config(command=lambda: click_button('8'))
button_nine.config(command=lambda: click_button('9'))
button_zero.config(command=lambda: click_button('0'))
button_plus.config(command=lambda: click_button('+'))
button_subtraction.config(command=lambda: click_button('-'))
button_multiply.config(command=lambda: click_button('*'))
button_division.config(command=lambda: click_button('/'))
button_dot.config(command=lambda: click_button('.'))

button_clear.config(command=clear)
button_equal.config(command=calculate)
button_back.config(command=back)

"""键盘事件"""


# 处理按钮功能
def press_button0(event=None):
    click_button('0')


def press_button1(event=None):
    click_button('1')


def press_button2(event=None):
    click_button('2')


def press_button3(event=None):
    click_button('3')


def press_button4(event=None):
    click_button('4')


def press_button5(event=None):
    click_button('5')


def press_button6(event=None):
    click_button('6')


def press_button7(event=None):
    click_button('7')


def press_button8(event=None):
    click_button('8')


def press_button9(event=None):
    click_button('9')


def press_button_plus(event=None):
    click_button('+')


def press_button_subtraction(event=None):
    click_button('-')


def press_button_division(event=None):
    click_button('/')


def press_button_multiply(event=None):
    click_button('*')


def press_button_dot(event=None):
    click_button('.')


# 计算，button_calculate的用法
def calculate1(event=None):
    calculate()


def back1(event=None):
    back()


def clear1(event=None):
    clear()


# 绑定按键和处理动作，其中1-5数字按键为特殊按钮，不能直接用<1>表示，而是<key-1>
root.bind("<Key-0>", press_button0)
root.bind("<Key-1>", press_button1)
root.bind("<Key-2>", press_button2)
root.bind("<Key-3>", press_button3)
root.bind("<Key-4>", press_button4)
root.bind("<Key-5>", press_button5)
root.bind("<Key-6>", press_button6)
root.bind("<Key-7>", press_button7)
root.bind("<Key-8>", press_button8)
root.bind("<Key-9>", press_button9)
root.bind("<equal>", press_button_plus)
root.bind("<minus>", press_button_subtraction)
root.bind("<*>", press_button_multiply)
root.bind("</>", press_button_division)
root.bind("<.>", press_button_dot)

"""因为是通过函数直接关联点击按钮处理事件，所以按钮无需再配置command"""
# button_zero.config(command=press_button0)
# button_one.config(command=press_button1)
# button_two.config(command=press_button2)
# button_three.config(command=press_button3)
# button_four.config(command=press_button4)
# button_five.config(command=press_button5)
# button_six.config(command=press_button6)
# button_seven.config(command=press_button7)
# button_eight.config(command=press_button8)
# button_nine.config(command=press_button9)
# button_plus.config(command=press_button_plus)
# button_subtraction.config(command=press_button_subtraction)
# button_multiply.config(command=press_button_multiply)
# button_division.config(command=press_button_division)
# button_dot.config(command=press_button_dot)

# button_two['command'] = press_button2

root.bind("<Return>", calculate1)
root.bind("<BackSpace>", back1)
root.bind("<c>", clear1)

button_equal.config(command=calculate1)
button_back.config(command=back1)
button_clear.config(command=clear1)


# 监测按键
def keyBack(evt):
    msg = f"您按下了{evt.char}, ASCII代码{evt.keycode}\n"
    msg += f"按键名称{evt.keysym}, 系统代码{evt.keysym_num}"
    txt.set(msg)


root.bind("<Key>", keyBack)

root.mainloop()  # 窗口加载
