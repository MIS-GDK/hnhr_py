import hashlib
import random
import re
import string

import cx_Oracle

Pass_result = ""


def pass_random_md5(passwd):
    # user_list = []
    # user_list.append(passwd)
    global Pass_result

    # 创建md5对象
    m = hashlib.md5()

    Pass_result = "".join(passwd)
    # print(Pass_result)
    utf_pass = Pass_result.encode(encoding="utf-8")
    m.update(utf_pass)
    pass_md5 = m.hexdigest()
    return pass_md5


def select_passwd():
    # 连接数据库
    # conn = cx_Oracle.connect("erpdatainput/j7OPm0%v6MXPSQoF@10.0.119.46:1521/hadb")
    # conn = cx_Oracle.connect("hrhnprod/Ww7v*SLuhrDJ@192.168.0.190:1525/HRHNDB")
    conn = cx_Oracle.connect("hrhnprod/9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")
    # engine = create_engine("oracle://hrhnprod:9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")
    # 获取cursor
    c = conn.cursor()

    sql1 = "SELECT * FROM gdk_account WHERE account = :account "
    # print(sql)
    try:
        pm = {":account": "gdk"}
        x1 = c.execute(sql1, pm)
        res = x1.fetchall()
        # print(res[:2])
        for data in res:
            # print(data)
            # pass_md5 = pass_random_md5(data[3])
            global Pass_result
            print("%s   %s   %s " % (data[1], data[2], data[3]))

        c.close()
        # 关闭连接
        # conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        c.close()
        conn.close()
        return


select_passwd()
# # print(pass_random_md5())
