import cx_Oracle
import logging


class HaiDian:
    def __init__(self, billno):
        self.billno = billno

    def update_database_interface(self):
        # 连接数据库
        conn = cx_Oracle.connect("h2_query_hn/MS@ABHs36O3zv9q!@10.0.0.196:1521/MDMDB")
        # 获取cursor
        c = conn.cursor()
        # 查询采购退货明细表中的原批发销售单头id，销售发票细单行id为空的行，也就是接口行状态异常的
        pm = {":billno": self.billno}
        sql = (
            "select a.rowid,a.reacceptno,a.rowno,a.batsaleno,a.batsalerowno "
            + "from d_reaccept_d a "
            + "where reacceptno in (:billno) "
        )
        # print(sql)
        try:
            x = c.execute(sql, pm)
            res = x.fetchall()
            for data in res:
                print(data)
                # logging.info(
                #     "---------------------------------------------------------------------------------------------"
                # )
                # logging.info("采购退货明细接口表相关信息: ")
                # logging.info("退仓申请单单号,行号,INCA销售发货单头ID,INCA销售发票明细ID")
                # logging.info(data[1:])
                final_data = self.conn_inca_database_data(int(data[3]), int(data[4]))
                if final_data:
                    print(final_data)
                    param = {":1": data[1], ":2": data[2], ":3": final_data[0][1]}
                    sql = "update d_Reaccept_d a set a.batsalerowno = :3  WHERE a.Reacceptno = :1 AND a.Rowno = :2"
                    x = c.execute(sql, param)
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

    def conn_inca_database_data(self, Salesid, Iodtlid):
        # 连接数据库
        # conn = cx_Oracle.connect("ERPDATAINPUT/hrhnDATA2016..@10.0.119.25:1521/HADB")
        conn = cx_Oracle.connect("hrhnprod/9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")
        # 获取cursor
        c = conn.cursor()
        # 查询INCA 销售发票管理(1079)功能，获取销售发货单头单ID和销售发票细单ID
        pm = {
            "Salesid": Salesid,
            "Iodtlid": Iodtlid,
        }
        sql = """
        SELECT b.Salesid, b.Sasettledtlid
            FROM Bms_Sa_Settle_Doc a, Bms_Sa_Settle_Dtl b
        WHERE a.Sasettleid = b.Sasettleid
            AND a.Salesid = {Salesid}
            AND b.Iodtlid = {Iodtlid}
        """
        sql2 = sql.format(**pm)
        try:
            # print(sql)
            x = c.execute(sql2)
            res = x.fetchall()
            c.close()
            conn.close()
            return res
        except Exception as e:
            print(str(e))
            conn.rollback()
            c.close()
            conn.close()
            return


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M",
    filename=r"E:/haidian_log.txt",
)
billno_list = ["122410070000428"]
for i in billno_list:
    test = HaiDian(i)
    test.update_database_interface()
