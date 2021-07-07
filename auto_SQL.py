import cx_Oracle
import datetime
import random
import string


class Auto_Sql:
    def Ar_Receipt_Match_interface(self):
        Receipt_Num = []
        # 上月最后一天
        last = datetime.date(
            datetime.date.today().year, datetime.date.today().month, 1
        ) - datetime.timedelta(1)
        # 连接数据库
        conn = cx_Oracle.connect("erpdatainput/j7OPm0%v6MXPSQoF@10.0.119.46:1521/HADB")
        # 获取cursor
        c = conn.cursor()
        # 查询发票接口中报 请打开本机构应收控制期间 相关错误的数据
        sql = (
            "SELECT Sd.Apply_Date,Sd.Gl_Date,Sd.Source_System_Code,Sd.Transaction_Header_Id,sd.Receipt_Num "
            + "FROM Crcdatafix.Hrhn_Erpom_20210102_400 Sd "
            + "WHERE Sd.Process_Status = 'E' "
            + "AND Sd.Source_System_Code = 'HNAS1' "
            + "AND Sd.Error_Msg LIKE '%请打开本机构应收控制期间%' "
            + "AND Sd.Apply_Date >= Trunc(SYSDATE, 'mm')"
        )
        sql2 = (
            "SELECT Sd.* "
            + "FROM Crcdatafix.Hrhn_Erpom_20210102_400 Sd "
            + "WHERE Sd.Process_Status = 'E' "
            + "AND Sd.Source_System_Code = 'HNAS1' "
            + "AND Sd.Error_Msg LIKE '%请打开本机构应收控制期间%' "
            + "AND Sd.Apply_Date >= Trunc(SYSDATE, 'mm');"
        )
        try:
            x = c.execute(sql)
            res = x.fetchall()
            count = 0
            for data in res:
                count = count + 1
                # print(data)
                if data[4] not in Receipt_Num:
                    Receipt_Num.append(data[4])
            ran_str = "".join(random.sample(string.ascii_letters + string.digits, 3))
            # print(ran_str)
            now = datetime.datetime.now().strftime("%Y_%m_%d_")
            print(
                "create table crcdatafix.hrhn_erpom_"
                + now
             + ran_str
                + "_bak as "
                + "\r"
                + sql2
            )
            print("\r")
            # print(now)
            print(
                "UPDATE Ogg.Cux_29_Ar_Receipt_Match_Iface a SET a.Gl_Date = %s , a.Apply_Date = %s WHERE Process_Status <> 'S' AND Receipt_Num IN ( %s );"
                % (
                    "to_date('" + str(last) + "','yyyymmdd')",
                    "to_date('" + str(last) + "','yyyymmdd')",
                    ", ".join("'{0}'".format(w) for w in Receipt_Num),
                )
            )
            print(count)
            # 关闭连接
            # conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            conn.rollback()
            c.close()
            conn.close()
            return


a = Auto_Sql()
a.Ar_Receipt_Match_interface()
