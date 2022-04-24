import logging
import logging.handlers
import cx_Oracle
import pyodbc


class Logsql:
    @staticmethod
    def log(loggername):
        # 创建logger，如果参数为空则返回root logger
        logger = logging.getLogger(loggername)
        logger.setLevel(logging.DEBUG)  # 设置logger日志等级
        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志

        if not logger.handlers:
            # 创建handler
            # fh = logging.FileHandler("sqllog.log", encoding="utf-8")
            # 日志文件按照大小分割
            fh = logging.handlers.RotatingFileHandler(
                "sqllog.log", maxBytes=20 * 1024 * 1024, backupCount=5
            )
            # ch = logging.StreamHandler()

            # 设置输出日志格式
            formatter = logging.Formatter(
                fmt="%(asctime)s %(name)s %(message)s",
                datefmt="%Y/%m/%d %X",
            )

            # 为handler指定输出格式
            fh.setFormatter(formatter)
            # ch.setFormatter(formatter)

            # 为logger添加的日志处理器
            logger.addHandler(fh)
            # logger.addHandler(ch)
        return logger  # 直接返回logger


class Mssql:
    def __init__(self):
        self.cur = None
        self.conn = None
        self.list1 = []

    def mssql_conn(self):
        try:
            self.conn = pyodbc.connect(
                "DRIVER={SQL Server};SERVER=192.168.0.165;DATABASE=suerp;UID=hrhn_suerp;PWD=OcZi2UktnEwM"
            )
            self.cur = self.conn.cursor()
            Logsql.log("msloger").debug("mssql connect success")
        except Exception as e:
            Logsql.log("msloger").debug("connect-error:%s", e)

        return self.conn, self.cur

    def mssql_select(self, sqlstr):
        try:
            self.cur.execute(sqlstr)
            # self.cur.executemany(sqlstr,[])
            self.list1 = self.cur.fetchall()
            # Logsql.log("msloger").debug("mssql select success:%s", len(self.list1))
            Logsql.log("msloger").debug("mssql select success")
        except Exception as e:
            Logsql.log("msloger").debug("select-error:%s", e)
        return self.list1

    def mssql_update(self, sqlstr, param_list):
        try:
            self.cur.executemany(sqlstr, param_list)
            self.conn.commit()
            # Logsql.log("msloger").debug("mssql update success:%s", param_list)
            Logsql.log("msloger").debug("mssql update success")
        except Exception as e:
            Logsql.log("msloger").debug("update-error:%s", e)
            self.conn.rollback()

    def mssql_close(self):
        try:
            self.cur.close()
            self.conn.close()
            Logsql.log("msloger").debug("ms close success")
        except Exception as e:
            Logsql.log("msloger").debug("close-error:%s", e)


class Oraclesql:
    def __init__(self, param_list):
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
            Logsql.log("oraclelogger").debug("update batchid list: ")
            for i in param_list:
                Logsql.log("oraclelogger").debug(i)
            return 1
        except Exception as e:
            Logsql.log("oraclelogger").debug("update-error:%s", e)
            self.conn.rollback()
            return 0

    def oracle_close(self):
        try:
            self.cur.close()
            self.conn.close()
            Logsql.log("oraclelogger").debug("oracle close success")
        except Exception as e:
            Logsql.log("oraclelogger").debug("close-error:%s", e)


if __name__ == "__main__":
    v_count = 1
    while v_count <= 5:
        new_mssql = Mssql()
        # 连接mssql执行查询
        new_mssql.mssql_conn()
        sqlstr1 = "select top 100 * from  SCAN_STATE_ERP where (FP_STATE = 'E' or SH_STATE = 'E' ) and UPD_STATE = '0'"
        list1 = new_mssql.mssql_select(sqlstr1)
        if list1:
            sqlstr2 = "UPDATE Bms_Batch_Def SET Invscanflag = (:1), Listscanflag = (:2) WHERE Batchid =(:3)"
            # 格式化处理
            val_fmt = lambda i: 1 if i == "E" else 0
            param_list = [
                (val_fmt(list1[i][3]), val_fmt(list1[i][4]), int(list1[i][2]))
                for i in range(len(list1))
            ]
            new_oracle = Oraclesql(param_list)
            # 连接oracle 执行更新
            new_oracle.oracle_conn()
            # 批发erp 批发表执行成功 更新两票制upd_state
            flag = new_oracle.oracle_execute(sqlstr2)
            if flag == 1:
                param_list2 = [("1", list1[i][0]) for i in range(len(list1))]
                sqlstr3 = "UPDATE SCAN_STATE_ERP SET upd_state = (?) WHERE row_id = (?)"
                new_mssql.mssql_update(sqlstr3, param_list2)
                # print(param_list2)
            new_oracle.oracle_close()
        else:
            new_mssql.mssql_close()
            break
        new_mssql.mssql_close()
        v_count += 1
