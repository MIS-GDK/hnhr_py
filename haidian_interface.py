import logging
import time

import cx_Oracle


class HaiDian:
    def __init__(self, billno):
        self.billno = billno

    def reaccept_update(self):
        pass

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
            + "and a.batsaleno is null "
            + "and a.batsalerowno is null"
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
                final_data = self.conn_haidian_database_data(data[1], data[2])
                if final_data:
                    print(t)
                    param = {
                        ":1": data[1],
                        ":2": data[2],
                        ":3": final_data[0][0],
                        ":4": final_data[0][1],
                    }
                    sql = "update d_Reaccept_d a set a.batsaleno = :3,a.batsalerowno = :4 WHERE a.Reacceptno = :1 AND a.Rowno = :2"
                    x = c.execute(sql, param)
                # if self.goodsinfo[4] > datetime.date(2019,12,1)
                else:
                    logging.info(
                        "DELETE FROM d_Reaccept_d a WHERE a.Reacceptno = '"
                        + str(data[1])
                        + "' AND a.Rowno = "
                        + str(data[2])
                        + ";"
                    )
                    logging.info(
                        "UPDATE d_Reaccept_h h SET h.Itemnums = h.Itemnums - 1 WHERE h.Reacceptno = '"
                        + str(data[1])
                        + "';"
                    )
                    # logging.info("COMMIT;")
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

    def conn_haidian_database_data(self, billno, rowno):
        # 连接数据库
        conn = cx_Oracle.connect("QUERY_HEN/AMm1!%KE7kmees09@10.0.0.201:1521/BJDB")
        # 获取cursor
        c = conn.cursor()
        # 查询采购退货明细表中的原批发销售单头id，销售发票细单行id为空的行，也就是接口行状态异常的
        pm = {":1": billno, ":2": rowno}
        # 根据采购退货接口表中异常未处理的行，查询退仓申请单表中相应的行信息
        sql = (
            "SELECT t.Warecode,d.Wareid,d.Batid, d.Srcstallno,d.Makeno,t.Warename,t.Warespec "
            + "FROM t_Distapply_d d, t_Distapply_h h,t_Ware t "
            + "WHERE d.Applyno = h.Applyno"
            + " AND h.Applyno = :1"
            + " AND d.Rowno = :2"
            + " AND t.Wareid = d.Wareid"
            + " AND t.Compid = h.Compid"
        )
        final_data = None
        try:
            # print(sql)
            x = c.execute(sql, pm)
            res = x.fetchone()
            # logging.info("退仓申请单相关信息:")
            # logging.info("商品编码,商品ID,批次,货位,批号,货品名称,规格")
            # logging.info(res)
            # print(res)
            # 根据退仓申请单信息 查询配送单相关信息
            param2 = {":3": res[2], ":4": res[1], ":5": res[4]}
            sql2 = (
                "SELECT h.Distno, h.Execdate, h.Notes "
                + "FROM t_Dist_d s, t_Dist_h h  "
                + "WHERE s.Batid = :3 "
                + "AND s.Wareid = :4 "
                + "AND s.Makeno = :5 "
                + "AND s.Distno = h.Distno "
                + "AND h.Notes LIKE '委托配送单%' "
                + "AND h.Billcode IN ('DIS', 'ADD')"
            )
            x2 = c.execute(sql2, param2)
            res2 = x.fetchone()
            # logging.info("配送单相关信息:")
            # logging.info("配送单号,生效时间,备注")
            # logging.info(res2)
            print(res2)
            if res2 and res2[2].find("委托配送单") != -1:
                t = res2[2][res2[2].find("：") + 1 : 14]
                final_data = self.conn_inca_database_data(
                    t, res[0], res[4], res[5], res[6]
                )
                # logging.info("INCA 销售发货单头单ID,销售发票管理细单ID")
                # logging.info(final_data)
            else:
                pass
                # print("this can't handle by program,please contact DBA")
                # logging.info("this can't handle by program,please contact DBA")

            c.close()
            # 关闭连接
            conn.close()
        except Exception:
            conn.rollback()
            c.close()
            # 关闭连接
            conn.close()
        return final_data

    def conn_inca_database_data(self, Salesid, Goodsno, Makeno, Goodsname, Goodstype):
        # 连接数据库
        # conn = cx_Oracle.connect("ERPDATAINPUT/hrhnDATA2016..@10.0.119.25:1521/HADB")
        conn = cx_Oracle.connect("hrhnprod/9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")
        # 获取cursor
        c = conn.cursor()
        # 查询INCA 销售发票管理(1079)功能，获取销售发货单头单ID和销售发票细单ID
        pm = {
            ":1": Salesid,
            ":2": Goodsno,
            ":3": Goodsname,
            ":4": Goodstype,
            ":5": Makeno,
        }
        sql = (
            "SELECT d.Salesid, d.Sasettledtlid"
            + " FROM Bms_Sa_Settle_Dtl_v d, Pub_Goods Peg"
            + " WHERE d.Salesid = :1"
            + " AND Peg.Goodsid = d.Goodsid"
            + " AND Peg.Goodsno = :2"
            + " AND d.Goodsname = :3"
            + " AND d.Goodstype = :4"
            + " AND d.Lotno = :5"
        )
        try:
            # print(sql)
            x = c.execute(sql, pm)
            res = x.fetchall()
            # print(res)
            c.close()
            conn.close()
            return res
        except Exception:
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
billno_list = ["122410220000345"]
for i in billno_list:
    test = HaiDian(i)
    test.update_database_interface()
