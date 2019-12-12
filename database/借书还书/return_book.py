import pymysql
import tkinter as tk
from tkinter import messagebox
from 界面 import user_window


def return_book(user_name, book_name):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zyy1154...',
        db='spider'
    )
    name_result = []
    status_result = []
    cursor = connect.cursor()
    cursor.execute(
        'select bookname, status from loantable where username= "' + user_name + '" and status="借出" '
    )
    result = cursor.fetchall()

    for i in range(len(result)):
        name_result.append(result[i][0])
        status_result.append(result[i][1])

    if user_window.isnull(book_name):
        tk.messagebox.showerror(title='错误提示', message='书名不能为空！')
    elif book_name not in name_result:
        tk.messagebox.showerror(title='错误提示', message='您没有借这本书！')
    else:
        tk.messagebox.showinfo(title='succeed', message='还书成功')
        cursor.execute(
            'update loantable set status="在库", username="无" where bookname="' + book_name + '"')

    connect.commit()
    cursor.close()
    connect.close()
