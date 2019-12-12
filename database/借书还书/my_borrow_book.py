import tkinter as tk
from tkinter import ttk
import pymysql


def check(username):
    window = tk.Tk()
    window.title('查看我借的书')
    # 设置窗口在屏幕正中间
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    ww = 850  # 宽度
    wh = 250  # 高度
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    frame = tk.Frame(window)
    frame.place(x=35, y=30, width=900, height=200)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(frame, columns=('书名', '作者', '出版社'), show="headings", yscrollcommand=scrollbar.set)

    tree.column('书名', width=320, anchor='center')
    tree.column('作者', width=220, anchor='center')
    tree.column('出版社', width=220, anchor='center')

    tree.heading('书名', text='书名')
    tree.heading('作者', text='作者')
    tree.heading('出版社', text='出版社')
    tree.pack(side=tk.LEFT, fill=tk.Y)
    scrollbar.config(command=tree.yview)

    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zyy1154...',
        db='spider'
    )

    name_result = []
    author_result = []
    press_result = []

    cursor = connect.cursor()
    cursor.execute(
        'select name,author,press from book,loantable where book.name=loantable.bookname'
        ' and username="' + username + '" and status="借出" ')
    result = cursor.fetchall()

    for i in range(len(result)):
        name_result.append(result[i][0])
        author_result.append(result[i][1])
        press_result.append(result[i][2])

    connect.commit()
    cursor.close()
    connect.close()

    for i in range(len(name_result)):
        tree.insert('', i, values=(name_result[i], author_result[i], press_result[i]))

    window.mainloop()
