import pymysql

conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='zyy1154...',
    db='spider'
)
cursor = conn.cursor()

conn.commit()
cursor.close()
conn.close()
