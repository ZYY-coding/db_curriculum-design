import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
import pymysql
from 借书还书 import borrow_book
from 借书还书 import my_borrow_book
from 借书还书 import return_book


def isnull(string):
    if string.strip() == '':
        return True
    else:
        return False


def search(sc_name, sc_writer, sc_press, sc_status, tree):
    """通过用户的查询条件将查询结果进行显示"""

    x = tree.get_children()
    for item in x:
        tree.delete(item)

    name_result = []
    author_result = []
    press_result = []
    status_result = []
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zyy1154...',
        db='spider'
    )
    cursor2 = connect.cursor()
    search_sql = 'select name,author,press,status from book,loantable where book.name=loantable.bookname'

    if isnull(sc_name) and isnull(sc_writer) and isnull(sc_press) and isnull(sc_status):
        pass
    if not (isnull(sc_name)):
        search_sql += " and name like '%{}%'".format(sc_name)
    if not (isnull(sc_writer)):
        search_sql += " and author like '%{}%'".format(sc_writer)
    if not (isnull(sc_press)):
        search_sql += " and press like '%{}%'".format(sc_press)
    if not (isnull(sc_status)):
        search_sql += " and status = '{}'".format(sc_status)
    cursor2.execute(search_sql)
    result = cursor2.fetchall()
    for i in range(len(result)):
        name_result.append(result[i][0])
        author_result.append(result[i][1])
        press_result.append(result[i][2])
        status_result.append(result[i][3])

    connect.commit()
    cursor2.close()
    connect.close()

    for i in range(len(name_result)):
        tree.insert('', i, values=(name_result[i], author_result[i], press_result[i], status_result[i]))


def create_table(user_name):
    user_window = tk.Tk()
    user_window.title('图书管理系统')
    # 设置窗口在屏幕正中间
    sw = user_window.winfo_screenwidth()
    sh = user_window.winfo_screenheight()
    ww = 950  # 宽度
    wh = 500  # 高度
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    user_window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    tk.Label(user_window, text='当前登录用户为:{}'.format(user_name), font=('Arial', 15)).place(x=300, y=10)
    tk.Label(user_window, text='请输入查询条件:', font=('Arial', 14)).place(x=10, y=50)

    tk.Label(user_window, text='书名:', font=('Arial', 14)).place(x=10, y=90)
    sc_name = tk.StringVar()
    entry_sc_name = tk.Entry(user_window, textvariable=sc_name, width=20)
    entry_sc_name.place(x=65, y=92)

    tk.Label(user_window, text='作者:', font=('Arial', 14)).place(x=220, y=90)
    sc_writer = tk.StringVar()
    entry_sc_writer = tk.Entry(user_window, textvariable=sc_writer, width=13)
    entry_sc_writer.place(x=275, y=92)

    tk.Label(user_window, text='出版社:', font=('Arial', 14)).place(x=380, y=90)
    sc_press = tk.StringVar()
    entry_sc_press = tk.Entry(user_window, textvariable=sc_press, width=15)
    entry_sc_press.place(x=450, y=92)

    tk.Label(user_window, text='状态:', font=('Arial', 14)).place(x=570, y=90)
    sc_status = tk.StringVar()
    entry_sc_status = tk.Entry(user_window, textvariable=sc_status, width=6)
    entry_sc_status.place(x=630, y=92)

    btn_search = tk.Button(user_window, text='查询',
                           command=lambda: search(sc_name.get(), sc_writer.get(), sc_press.get(), sc_status.get(),
                                                  tree))
    btn_search.place(x=700, y=87)

    btn_borrow = tk.Button(user_window, text='借书', command=lambda: borrow_book.borrow(user_name, sc_name.get()))
    btn_borrow.place(x=750, y=87)

    btn_return = tk.Button(user_window, text='查看我借的书', command=lambda: my_borrow_book.check(user_name))
    btn_return.place(x=800, y=87)

    btn_borrow = tk.Button(user_window, text='还书', command=lambda: return_book.return_book(user_name, sc_name.get()))
    btn_borrow.place(x=890, y=87)

    frame = tk.Frame(user_window)
    frame.place(x=50, y=150, width=900, height=280)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(frame, columns=('书名', '作者', '出版社', '状态'), show="headings", yscrollcommand=scrollbar.set)

    tree.column('书名', width=320, anchor='center')
    tree.column('作者', width=220, anchor='center')
    tree.column('出版社', width=220, anchor='center')
    tree.column('状态', width=50, anchor='center')

    # 设置每列表头标题文本
    tree.heading('书名', text='书名')
    tree.heading('作者', text='作者')
    tree.heading('出版社', text='出版社')
    tree.heading('状态', text='状态')
    tree.pack(side=tkinter.LEFT, fill=tkinter.Y)
    scrollbar.config(command=tree.yview)

    user_window.mainloop()
