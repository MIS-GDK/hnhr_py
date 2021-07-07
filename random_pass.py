import random
import string
import re
import hashlib
import cx_Oracle

Pass_result = ""


def pass_random_md5():
    user_list = []
    global Pass_result
    punctuation = string.punctuation
    punctuation = punctuation.replace("&", "")
    for i in range(12):
        Your_pass = random.choice(string.ascii_letters + string.digits + punctuation)
        user_list.append(Your_pass)

    # 创建md5对象
    m = hashlib.md5()

    Pass_result = "".join(user_list)
    # print(Pass_result)
    utf_pass = Pass_result.encode(encoding="utf-8")
    m.update(utf_pass)
    pass_md5 = m.hexdigest()
    return pass_md5


def update_database_update():
    # 连接数据库
    # conn = cx_Oracle.connect("erpdatainput/j7OPm0%v6MXPSQoF@10.0.119.46:1521/hadb")
    conn = cx_Oracle.connect("hrhnprod/Ww7v*SLuhrDJ@192.168.0.190:1525/HRHNDB")
    # 获取cursor
    c = conn.cursor()

    sql1 = "SELECT Pe.Employeeid FROM Pub_Employee Pe WHERE Pe.Employeeid IN (37725) AND Pe.Usestatus = 1"

    sql2 = "update Pub_Employee pe set pe.webpass = :pass,pe.md5count=1,pe.leavejobstatus=0 where pe.employeeid = :id"
    # print(sql)
    try:
        x1 = c.execute(sql1)
        res = x1.fetchall()
        # print(res[:2])
        for data in res:
            pass_md5 = pass_random_md5()
            global Pass_result
            print("%s   %s   %s" % (data[0], Pass_result, pass_md5))
            pm = {":pass": pass_md5, ":id": data[0]}
            x2 = c.execute(sql2, pm)

        c.close()

        # 关闭连接
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        c.close()
        conn.close()
        return


update_database_update()
# print(pass_random_md5())
