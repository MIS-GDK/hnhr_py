import cx_Oracle
from two_invoice import Logsql


class Oraclesql:
    def __init__(self, param_list=None):
        self.cur = None
        self.conn = None
        self.param_list = param_list

    def oracle_conn(self):
        try:
            self.conn = cx_Oracle.connect(
                "erpdatainput/j7OPm0%v6MXPSQoF@10.0.119.46:1521/HADB"
            )
            self.cur = self.conn.cursor()
            Logsql.log("oraclelogger").debug("oracle_conn connect success")
        except Exception as e:
            Logsql.log("oraclelogger").debug("connect-error:%s", e)

        return self.conn, self.cur

    def oracle_execute(self, sqlstr):
        try:
            self.cur.executemany(sqlstr, self.param_list)
            # self.cur.execute(sqlstr, self.param_list)
            self.conn.commit()
            # Logsql.log("oraclelogger").debug(
            #     "oraclesql update success:%s", self.param_list
            # )
            Logsql.log("oraclelogger").debug("oraclesql update success")
            return 1
        except Exception as e:
            Logsql.log("oraclelogger").debug("update-error:%s", e)
            self.conn.rollback()
            return 0

    def oracle_select(self, sqlstr):
        try:
            self.cur.execute(sqlstr)
            list1 = self.cur.fetchall()
            Logsql.log("oracleloger").debug("oraclesql select success")
        except Exception as e:
            Logsql.log("oracleloger").debug("select-error:%s", e)
        return list1

    def oracle_close(self):
        try:
            self.cur.close()
            self.conn.close()
            Logsql.log("oraclelogger").debug("oracle close success")
        except Exception as e:
            Logsql.log("oraclelogger").debug("close-error:%s", e)


if __name__ == "__main__":
    sqlstr = "SELECT MAX(b.Credate) FROM Bms_Sa_Doc_v b, Bms_Sa_Dtl_v c WHERE b.Entryname = (:1) AND b.Salesid = c.Salesid AND c.Goodsno = (:2) AND b.Usestatus = 1 AND b.Satypeid = 1"
    # 格式化处理
    val_fmt = lambda i: 1 if i == "E" else 0
    new_oracle = Oraclesql()
    # 连接oracle 执行更新
    new_oracle.oracle_conn()
    # 批发erp 批发表执行成功 更新两票制upd_state
    flag = new_oracle.oracle_execute(sqlstr)
    new_oracle.oracle_close()