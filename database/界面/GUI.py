import tkinter as tk
import tkinter.messagebox
import pymysql
from 界面 import user_window
from 界面 import admin_window

# 创建登录主窗口
window = tk.Tk()
window.title('图书管理系统')
# 设置窗口在屏幕正中间
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
ww = 500
wh = 400
x = (sw - ww) / 2
y = (sh - wh) / 2
window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

# 插入图片
canvas = tk.Canvas(window, bg='white', height=130, width=500)
canvas.pack(side='top')
image_file = tk.PhotoImage(file='book.gif')
image = canvas.create_image(250, 0, anchor='center', image=image_file)

tk.Label(window, text='图书管理系统', font=('Arial', 20)).pack()
tk.Label(window, text='用户名:', font=('Arial', 14)).place(x=70, y=190)
tk.Label(window, text='密   码:', font=('Arial', 14)).place(x=70, y=230)

# 用户名
user_name = tk.StringVar()
entry_user_name = tk.Entry(window, textvariable=user_name, font=('Arial', 14))
entry_user_name.place(x=150, y=195)

# 用户密码
user_password = tk.StringVar()
entry_user_password = tk.Entry(window, textvariable=user_password, font=('Arial', 14), show='*')
entry_user_password.place(x=150, y=235)

user_name_list = []
user_password_list = []
user_authority_list = []


def login():
    """登录功能的实现"""

    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zyy1154...',
        db='spider'
    )
    cursor = conn.cursor()
    cursor.execute('select * from userinfo')
    result = cursor.fetchall()
    for i in range(len(result)):
        user_name_list.append(result[i][0])
        user_password_list.append(result[i][1])
        user_authority_list.append(result[i][2])

    conn.commit()
    cursor.close()
    conn.close()

    name = user_name.get()
    password = user_password.get()
    index = 0
    if name.strip() == '':
        tk.messagebox.showerror(title='错误提示', message='用户名不能为空！')
    elif password.strip() == '':
        tk.messagebox.showerror(title='错误提示', message='密码不能为空！')
    else:
        if name not in user_name_list:
            tk.messagebox.showerror(title='错误提示', message='用户名不存在！')
        else:
            for j in range(len(user_name_list)):
                if name == user_name_list[j]:
                    index = j
                    break
            if password == user_password_list[index] and user_authority_list[index] == "user":
                tkinter.messagebox.showinfo(title='welcome', message='用户{}登陆成功！'.format(user_name_list[index]))
                window.destroy()
                user_window.create_table(user_name.get())
            elif password == user_password_list[index] and user_authority_list[index] == "admin":
                tkinter.messagebox.showinfo(title='welcome', message='管理员{}登陆成功！'.format(user_name_list[index]))
                window.destroy()
                admin_window.create_table()
            else:
                tkinter.messagebox.showerror(title='错误提示', message='密码错误！')


# 登录按钮
btn_login = tk.Button(window, text='登录', command=login)
btn_login.place(x=180, y=290)


def reset():
    entry_user_password.delete(0, tk.END)
    entry_user_name.delete(0, tk.END)


# 重置按钮
btn_reset = tk.Button(window, text='重置', command=reset)
btn_reset.place(x=240, y=290)


def signup():
    """生成新的注册窗口"""
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry("%dx%d+%d+%d" % (300, 200, x + 90, y + 100))
    window_sign_up.title('注册')

    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='用户名: ').place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)
    entry_new_name.place(x=80, y=10)

    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='密码: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=80, y=50)

    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='确认密码: ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=80, y=90)

    def sign_to_db():
        """点击注册按钮可以把注册信息写入数据库"""
        conn = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='zyy1154...',
            db='spider'
        )
        cursor = conn.cursor()

        nn = new_name.get()
        np = new_pwd.get()
        npc = new_pwd_confirm.get()
        if nn.strip() == '':
            tk.messagebox.showerror(title='错误提示', message='用户名不能为空！')
        elif np.strip() == '':
            tk.messagebox.showerror(title='错误提示', message='密码不能为空！')
        elif nn in user_name_list:
            tkinter.messagebox.showerror('错误提示', '用户名已存在!')
        elif np != npc:
            tkinter.messagebox.showerror('错误提示', '密码和确认密码不相同！')
        else:
            sql = 'insert into userinfo VALUES(%s,%s,%s) '
            cursor.execute(sql, (nn, np, "user"))
            tkinter.messagebox.showinfo('welcome', '注册成功!')
            window_sign_up.destroy()

        conn.commit()
        cursor.close()
        conn.close()

    btn_confirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to_db)
    btn_confirm_sign_up.place(x=100, y=120)

    def inner_reset():
        entry_new_name.delete(0, tk.END)
        entry_usr_pwd.delete(0, tk.END)
        entry_usr_pwd_confirm.delete(0, tk.END)

    btn_reset_ = tk.Button(window_sign_up, text='重置', command=inner_reset)
    btn_reset_.place(x=150, y=120)


# 注册按钮
btn_sign_up = tk.Button(window, text='注册', command=signup)
btn_sign_up.place(x=300, y=290)

window.mainloop()
