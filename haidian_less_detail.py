import cx_Oracle
import logging
import time


class Handle_Less:
    def __init__(self, billno):
        self.billno = billno

    def update_haidian_interface(self, flag: int):
        if flag == 1:
            conn = cx_Oracle.connect(
                "h2_query_hn/MS@ABHs36O3zv9q!@10.0.0.196:1521/MDMDB"
            )
            cur = conn.cursor()
        else:
            conn = cx_Oracle.connect(
                "erpdatainput/j7OPm0%v6MXPSQoF@10.0.119.46:1521/hadb"
            )
            cur = conn.cursor()

        return conn, cur

    def select_haidian_interface(self, flag: int):
        conn, cur = self.update_haidian_interface(flag)
        sql = "SELECT a.* FROM d_Intent_d a WHERE a.Intentno in ({})".format(
            ",".join(["'%s'" % item for item in self.billno])
        )
        print(sql)

        try:
            x = cur.execute(sql)
            res = x.fetchall()
            print(res)
            cur.close()
            conn.close()
        except Exception:
            conn.rollback()
            cur.close()
            conn.close()
            return


billno = ["1221032201353", "121709010055295"]
HL = Handle_Less(billno)
HL.select_haidian_interface(1)