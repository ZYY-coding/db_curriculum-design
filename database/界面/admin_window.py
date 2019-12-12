import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
import tkinter.messagebox
import pymysql
from 界面 import user_window


def create_table():
    admin_window = tk.Tk()
    admin_window.title('图书管理系统')
    # 设置窗口在屏幕正中间
    sw = admin_window.winfo_screenwidth()
    sh = admin_window.winfo_screenheight()
    ww = 950  # 宽度
    wh = 500  # 高度
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    admin_window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    tk.Label(admin_window, text='当前身份是管理员，具有添加删除和查询的权限', font=('Arial', 15)).place(x=270, y=10)
    # 书名
    tk.Label(admin_window, text='书名:', font=('Arial', 14)).place(x=10, y=90)
    sc_name = tk.StringVar()
    entry_sc_name = tk.Entry(admin_window, textvariable=sc_name, width=20)
    entry_sc_name.place(x=65, y=92)
    # 作者
    tk.Label(admin_window, text='作者:', font=('Arial', 14)).place(x=220, y=90)
    sc_writer = tk.StringVar()
    entry_sc_writer = tk.Entry(admin_window, textvariable=sc_writer, width=13)
    entry_sc_writer.place(x=275, y=92)
    # 出版社
    tk.Label(admin_window, text='出版社:', font=('Arial', 14)).place(x=380, y=90)
    sc_press = tk.StringVar()
    entry_sc_press = tk.Entry(admin_window, textvariable=sc_press, width=15)
    entry_sc_press.place(x=450, y=92)
    # 状态
    tk.Label(admin_window, text='状态:', font=('Arial', 14)).place(x=570, y=90)
    sc_status = tk.StringVar()
    entry_sc_status = tk.Entry(admin_window, textvariable=sc_status, width=6)
    entry_sc_status.place(x=630, y=92)
    # 查询按钮
    btn_search = tk.Button(admin_window, text='查询',
                           command=lambda: user_window.search(sc_name.get(), sc_writer.get(), sc_press.get(),
                                                              sc_status.get(),
                                                              tree))
    btn_search.place(x=700, y=87)
    # 插入按钮
    btn_insert = tk.Button(admin_window, text='插入',
                           command=lambda: insert(sc_name.get(), sc_writer.get(), sc_press.get()))
    btn_insert.place(x=750, y=87)
    # 删除按钮
    btn_delete = tk.Button(admin_window, text='删除',
                           command=lambda: delete(sc_name.get(), tree))

    btn_delete.place(x=800, y=87)
    # 修改按钮
    # btn_modify = tk.Button(admin_window, text='修改', command=lambda: create_modify_window(sc_name.get()))
    # btn_modify.place(x=845, y=87)
    # 重置按钮
    btn_reset = tk.Button(admin_window, text='重置',
                          command=lambda: reset(entry_sc_name, entry_sc_writer, entry_sc_press))
    btn_reset.place(x=845, y=87)
    # 下面是显示查询结果的代码
    frame = tk.Frame(admin_window)
    frame.place(x=50, y=150, width=900, height=280)

    scrollbar = tkinter.Scrollbar(frame)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

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

    admin_window.mainloop()


def insert(sc_name, sc_writer, sc_press):
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zyy1154...',
        db='spider'
    )
    name_result = []
    cursor3 = connect.cursor()
    cursor3.execute('select name from book')
    result = cursor3.fetchall()
    for i in range(len(result)):
        name_result.append(result[i][0])
    if user_window.isnull(sc_name):
        tk.messagebox.showerror(title='错误提示', message='书名不能为空！')
    elif sc_name in name_result:
        tk.messagebox.showerror(title='错误提示', message='该书已经存在！')
    else:
        book_sql = 'insert into book values(%s,%s,%s)'
        connect.commit()
        loantable_sql = 'insert into loantable values(%s,%s,%s)'
        cursor3.execute(book_sql, (sc_name, sc_writer, sc_press))
        cursor3.execute(loantable_sql, (sc_name, "在库", '无'))
        tkinter.messagebox.showinfo(title='succeed', message='插入成功!')
    connect.commit()
    cursor3.close()
    connect.close()


def delete(sc_name, tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)

    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zyy1154...',
        db='spider'
    )
    cursor3 = connect.cursor()
    name_result = []
    author_result = []
    press_result = []
    status_result = []
    index = 0
    cursor3.execute('select name,status from book,loantable where book.name=loantable.bookname')
    result = cursor3.fetchall()
    for i in range(len(result)):
        name_result.append(result[i][0])
        status_result.append(result[i][1])
    for j in range(len(name_result)):
        if sc_name == name_result[j]:
            index = j
            break
    if user_window.isnull(sc_name):
        tkinter.messagebox.showerror(title='错误提示', message='书名不能为空!')
    elif sc_name not in name_result:
        tkinter.messagebox.showerror(title='错误提示', message='该书不存在!')
    elif status_result[index] == "借出":
        tkinter.messagebox.showerror(title='错误提示', message='该书被借出，不能删除!')
    else:
        cursor3.execute("delete from loantable where bookname='" + sc_name + "'")
        cursor3.execute("delete from book where name='" + sc_name + "'")
        tkinter.messagebox.showinfo(title='succeed', message='删除成功!')
        name_result.clear()
        status_result.clear()
        cursor3.execute('select name,author,press,status from book,loantable where book.name=loantable.bookname')
        result = cursor3.fetchall()
        for i in range(len(result)):
            name_result.append(result[i][0])
            author_result.append(result[i][1])
            press_result.append(result[i][2])
            status_result.append(result[i][3])
        for i in range(len(name_result)):
            tree.insert('', i, values=(name_result[i], author_result[i], press_result[i], status_result[i]))

    connect.commit()
    cursor3.close()
    connect.close()


# def create_modify_window():
#     """这个函数当点击用户界面的修改按钮后触发"""
#     modify_window = tk.Tk()
#     modify_window.title('图书信息修改')
#     sw = modify_window.winfo_screenwidth()
#     sh = modify_window.winfo_screenheight()
#     ww = 400  # 宽度
#     wh = 200  # 高度
#     x = (sw - ww) / 2
#     y = (sh - wh) / 2
#     modify_window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
#
#     tk.Label(modify_window, text='当前正在修改《{}》的信息'.format(sc_name), font=('Arial', 10)).place(x=40, y=20)
#     # 输入新的作者信息
#     tk.Label(modify_window, text='将作者改为:', font=('Arial', 14)).place(x=50, y=70)
#     new_author = tk.StringVar()
#     entry_new_author = tk.Entry(modify_window, textvariable=new_author, width=15)
#     entry_new_author.place(x=200, y=70)
#     # 输入新的出版社信息
#     tk.Label(modify_window, text='将出版社改为:', font=('Arial', 14)).place(x=50, y=110)
#     new_press = tk.StringVar()
#     entry_new_press = tk.Entry(modify_window, textvariable=new_press, width=15)
#     entry_new_press.place(x=200, y=110)
#
#     # 修改按钮
#     btn_modify = tk.Button(modify_window, text='修改', width=5,
#                            command=click_button)  # 将修改窗口里的作者和出版社信息传递给修改按钮绑定的函数
#     btn_modify.place(x=230, y=150)
#
#     modify_window.mainloop()


# def modify():
#     """这个函数当点击修改窗口中的修改按钮后触发"""
#     conn = pymysql.Connect(
#         host='localhost',
#         port=3306,
#         user='root',
#         passwd='zyy1154...',
#         db='spider'
#     )
#     cursor = conn.cursor()
#
#     if user_window.isnull(new_author.get()):
#         tkinter.messagebox.showerror(title='错误提示', message='修改后的作者不能为空!')
#     elif user_window.isnull(new_press.get()):
#         tkinter.messagebox.showerror(title='错误提示', message='修改后的出版社不能为空!')
#     else:
#         cursor.execute("update book set author='" + new_author.get() + "'where name='" + sc_name + "'")
#         cursor.execute("update book set press='" + new_press.get() + "'where name='" + sc_name + "'")
#         tkinter.messagebox.showinfo(title='succeed', message='修改成功')
#         modify_window.destroy()
#         conn.commit()
#         cursor.close()
#         conn.close()


def reset(entry_1, entry_2, entry_3):
    entry_1.delete(0, tk.END)
    entry_2.delete(0, tk.END)
    entry_3.delete(0, tk.END)
