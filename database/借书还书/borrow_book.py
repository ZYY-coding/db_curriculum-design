import tkinter as tk
import pymysql
from tkinter import messagebox

"""借书功能存在的问题：如果从用户登录开始的话，总会错误提示该书不存在，检查发现是book_name参数传递出了问题
   但直接运行借书的界面就能借书，这是怎么回事？
   wdnmd不再新建窗体了，直接在查询界面一键借书就行了
"""


def create_window(user_name):
    window = tk.Tk()
    window.title('借书')
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    ww = 250
    wh = 120
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    tk.Label(window, text='请输入要借的图书:', font=('Arial', 14)).place(x=10, y=20)

    book = tk.StringVar()
    name_input = tk.Entry(window, textvariable=book, width=30)
    name_input.place(x=10, y=50)

    btn_borrow = tk.Button(window, text='借书', command=lambda: borrow(user_name, book.get()))
    btn_borrow.place(x=100, y=85)
    window.mainloop()


def borrow(user_name, book_name):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zyy1154...',
        db='spider'
    )
    cursor = connect.cursor()

    index = 0
    name_result = []
    status_result = []
    search_sql = 'select bookname,status from loantable'
    cursor.execute(search_sql)
    result = cursor.fetchall()
    for i in range(len(result)):
        name_result.append(result[i][0])
        status_result.append(result[i][1])

    for j in range(len(name_result)):
        if book_name == name_result[j]:
            index = j
            break
    if book_name not in name_result:
        tk.messagebox.showerror(title='错误提示', message='该书不存在!')
    elif status_result[index] == '借出':
        tk.messagebox.showerror(title='错误提示', message='该书被借出!')
    else:
        tk.messagebox.showinfo(title='succeed', message='借书成功')
        cursor.execute(
            'update loantable set status="借出", username="' + user_name + '" where bookname="' + book_name + '"')

    connect.commit()
    cursor.close()
    connect.close()


