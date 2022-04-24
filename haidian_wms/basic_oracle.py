import logging
import logging.handlers
import time
import cx_Oracle
import re
from datetime import datetime


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
                "sqllog.log", maxBytes=20 * 1024 * 1024, backupCount=5, encoding="utf-8"
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


class oracleCode:
    def __init__(self, database, param_list):
        self.cur = None
        self.conn = None
        self.database = database
        self.param_list = param_list
        # 配送申请单 查询海典中间库 sql
        self.delivery_sqlstr = (
            "SELECT Proof_Id,Src_Proof_Id,Src_Line_Id,Sale_Type,Proof_Date,Customer_Id,Goods_Id,Lot_No,Batch_No,Valid_Date,"
            + "Product_Date,'' Quantitybak,Price,Goods_Amount,Ws_Price,Rt_Price,Discount,Real_Price,Warehost_Id,Bill_Style,Proof_Human,"
            + "Do_Man,Chk_Man,Tax,Tax_Per,Amount_Tax,Get_Date,Proof_Style,Client_Style,Memo,Bill_Level,Send_Time,Company_Id,Drug_Supervise_Sn,"
            + "Buy_Price,Payment_Type,'0' State,Quality_Flag, Account_Flag,Memo_File1,Memo_File2,Memo_File3,Monomark,Depart_Id2,Owner_Id,"
            + "'' Create_Man,Create_Org,SYSDATE Create_Date,'' Modify_Man,SYSDATE Modify_Date,'0' Isdeleted,Create_Orgseq,Create_Role,Org_Id,"
            + "Warehouse_Type,Add_Id,Goodssys_Id,Customersys_Id,Haulingtrack,Yaojian_Flag,Upd_State,Goods_Pc_Killbac,Proof_Lines,Largess_Flage,"
            + "Distlevel,Bill_Type,Bill_Flag,Bill_Srcproofid,Goods_Flag,Trans_Type,Upd_Mode,Quantity,Buyplan_Src_Line_Id,Buyplan_Src_Proof_Id,"
            + "Salle_Batchnums,Put_Flag,Container_Id,Container_Name,Dtz,Memo_File4,Memo_File5,Memo_File6,Memo_File7,Memo_File8,Memo_File9,Memo_File10,"
            + "'0' Gsk_State,'' Gsk_Memo,'' Gsk_Date"
            + " FROM Erpsaleproof@Wms"
            + " WHERE Src_Proof_Id like '%'||:1 and Upd_State = '0'"
        )
        self.purchase_sqlstr = (
            "SELECT '' Proof_Id,Src_Proof_Id,Src_Line_Id,Supplier_Id,Goods_Id,Buy_Price,Quantity,0 Land_Qty,"
            + "Piece,Amount,'0' State,Confirm_Man,Confirm_Date,'' Isused_Flag,Proof_Man,Proof_Date,'' Print_Flag,Order_Flag,"
            + "Complete_Date,Memo,Owner_Id,Create_Man,Create_Role,SYSDATE Create_Date,'' Modify_Man,'' Modify_Date,'0' Isdeleted,"
            + "Create_Orgseq,Create_Org,Org_Id,Stockcalgroup_Id,Receive_Type,Batch_No,Valid_Date,Product_Date,'' Bp_Transportunit,'' Bp_Modeoftransport,"
            + "'' Bp_Arrivaltime,'' Bp_Timeintransit,'' Bp_Timeofdeparture,'' Bp_Isagreement,'' Bp_Ypplaceoforigin,'' Bp_Sendaddress,To_Proof_Id,"
            + "To_Line_Id,Bill_Flag,'' Contract,'' In_Style,'' Rt_Price,Upd_Mode,Goods_Pc_Killbac,Supplier_Sdth_Id,Invoice_Type,Memo_File1,"
            + "Memo_File2,Memo_File3,'' Send_Manifest_Id,Special_Flag,Payment_Flag,'' License,'' Mah_Owner,'' Manufacturing_Site,Add_Id,"
            + "'' Ips_Saleproof_Confirm_State,'' Ips_Saleproof_Confirm_Date,'' Th_Senddepartdate,'' Th_Sjjg,'' Th_Transportedate"
            + " FROM Erpbuyplan@Wms"
            + " WHERE Src_Proof_Id LIKE 'YBQXINT'|| :1"
        )
        self.oper_sqlstr = (
            "SELECT Src_Proof_Id,Src_Line_Id,Task_Type,Stockcalgroup_Id,State,Client_Id,Create_Date,Modify_Man,"
            + "Modify_Date,'',Collection_Id,Isdeleted,Org_Id,Owner_Id,Create_Org,Create_Orgseq,Upd_State,Upd_Mode,Upd_Date,Opt_Date,Remark,Row_Id "
            + " FROM Operate_Log s"
            + " WHERE s.Src_Proof_Id LIKE '%'||:1"
        )
        self.oper_task_sqlstr = (
            "select Task_Id,Src_Order_Id,Src_Proof_Id,Src_Line_Id,order_type,Stockcalgroup_Id,Src_Loc_Id,Operatecase_Qty,Operate_Qty,State,Container_Id,"
            + "Container_Index,Lot_No,Goods_Id,Batch_No,Goods_Pc_Killbac,Valid_Date,Product_Date,Realcase_Qty,Real_Qty,Client_Id,Company_Id,Casing_Id,"
            + "Operate_Date,Operate_Man,Complete_Date,Create_Man,Create_Date,Modify_Man,Modify_Date,Warehouse_Type,Collection_Id,Isdeleted,Org_Id,"
            + "Owner_Id,Create_Org,Create_Orgseq,Upd_State,Upd_Mode,Upd_Date,Opt_Date,Remark,Row_Id,'' Conclusion,'' Batorderno,'' Hydee_Update,'' Qualityerport_Id,"
            + " '' Proof_Remark,'' Goods_Pc_Date,Src_Task_Id,'','','','','','','',''"
            + " FROM Operate_Task_Log s"
            + " WHERE s.Src_Proof_Id LIKE '%'||:1"
        )
        self.state_sqlstr = (
            "SELECT Client_Id,Src_Order_Id,Create_Date,Create_Org,Create_Orgseq,Isdeleted,Org_Id,Owner_Id,"
            + "Stockcalgroup_Id,Order_Type,Opt_Date,Upd_Date,Upd_Mode,Upd_State,Remark,Row_Id,''"
            + " FROM Operate_Task_Log s"
            + " WHERE s.Src_Proof_Id LIKE '%'||:1"
        )

        # 配送申请单 插入wms sql
        self.delivery_insert_sqlstr = None
        # 采购订单 插入wms sql
        self.purchase_insert_sqlstr = None

    def oracle_conn(self):
        try:
            if self.database == "haidian":
                self.conn = cx_Oracle.connect(
                    "query_hen/AMm1!%KE7kmees09@10.0.0.201:1521/bjdb"
                )
                self.cur = self.conn.cursor()
                Logsql.log("databaseLogger").debug(self.database + " connect success")
            elif self.database == "wms":
                self.conn = cx_Oracle.connect(
                    "orawms/Y=y018*QD[L9c@172.18.31.1:1521/zzora"
                )
                self.cur = self.conn.cursor()
                Logsql.log("databaseLogger").debug(self.database + " connect success")

        except Exception as e:
            Logsql.log("databaseLogger").debug(self.database + " connect-error:%s", e)

        return self.conn, self.cur

    def oracle_select(self, sqlstr, pm):
        list1 = []
        try:
            self.cur.execute(sqlstr, pm)
            list1 = self.cur.fetchall()
            Logsql.log("databaseLogger").debug(self.database + " select success")
        except Exception as e:
            Logsql.log("databaseLogger").debug(self.database + " select-error:%s", e)
        return list1

    def oracle_execute(self, sqlstr, pm):
        try:
            self.cur.execute(sqlstr, pm)
            self.conn.commit()
            Logsql.log("databaseLogger").debug(self.database + " execute success")
        except Exception as e:
            Logsql.log("databaseLogger").debug(self.database + " execute-error:%s", e)
            self.conn.rollback()

    def oracle_close(self):
        try:
            self.cur.close()
            self.conn.close()
            Logsql.log("databaseLogger").debug(self.database + " close success")
        except Exception as e:
            Logsql.log("databaseLogger").debug(self.database + " close-error:%s", e)

    """
    配送申请单 海典 传送到 wms,需要将中间库数据 写入到wms
    """

    def delivery_apply(self, sqlstr, new_wms):
        for i in self.param_list:
            pm = {":1": i}
            print(pm)
            mylist1 = self.oracle_select(sqlstr, pm)
            Logsql.log("databaseLogger").debug(
                self.database + " salesnumber: " + str(mylist1)
            )
            if mylist1:
                for i in range(0, len(mylist1)):
                    datalist1 = list(mylist1[i])
                    # 找到列表中的 datetime.datetime
                    for j in range(len(datalist1)):
                        if type(datalist1[j]) == datetime:
                            datalist1[
                                j
                            ] = "to_date('%s','yyyy-MM-dd hh24:mi:ss')" % datalist1[
                                j
                            ].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                    datalast = []
                    datalast.append(tuple(datalist1))
                    # 组装插入语句
                    sql1 = (
                        "INSERT INTO Saleproof VALUES %r" % tuple(datalast)
                    ).replace("None", "null")

                    # 正则表达式 去除sql中 日期两端的 双引号
                    self.delivery_insert_sqlstr = re.sub('"', "", sql1)
                    try:
                        new_wms.cur.execute(self.delivery_insert_sqlstr)
                        new_wms.conn.commit()
                        Logsql.log("databaseLogger").debug(
                            new_wms.database + " wms insert success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            new_wms.database + " insert-error:%s", e
                        )
                    try:
                        sql_update = "update Erpsaleproof@Wms set upd_state = 'E' where Src_Proof_Id = :1"
                        self.oracle_execute(sql_update, pm)
                        Logsql.log("databaseLogger").debug(
                            self.database + " delivery_apply haidian update success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            self.database + " update-error:%s", e
                        )

    """
    采购订单 海典 传送到 wms,需要将中间库数据 写入到wms
    """

    def purchase_apply(self, sqlstr, new_wms):
        for i in self.param_list:
            pm = {":1": i}
            # print(pm)
            mylist1 = self.oracle_select(sqlstr, pm)
            Logsql.log("databaseLogger").debug(
                self.database + " purchasenumber: " + str(mylist1)
            )
            if mylist1:
                for i in range(0, len(mylist1)):
                    datalist1 = list(mylist1[i])
                    # 找到列表中的 datetime.datetime
                    for j in range(len(datalist1)):
                        if type(datalist1[j]) == datetime:
                            datalist1[
                                j
                            ] = "to_date('%s','yyyy-MM-dd hh24:mi:ss')" % datalist1[
                                j
                            ].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                    datalast = []
                    datalast.append(tuple(datalist1))
                    # 组装插入语句
                    sql1 = (
                        "INSERT INTO C_BUYPLAN VALUES %r" % tuple(datalast)
                    ).replace("None", "null")

                    # 正则表达式 去除sql中 日期两端的 双引号
                    self.purchase_insert_sqlstr = re.sub('"', "", sql1)
                    # print(self.purchase_insert_sqlstr)
                    try:
                        new_wms.cur.execute(self.purchase_insert_sqlstr)
                        new_wms.conn.commit()
                        Logsql.log("databaseLogger").debug(
                            new_wms.database + " wms insert success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            new_wms.database + " insert-error:%s", e
                        )
                    try:
                        sql_update = "update Erpbuyplan@Wms set upd_state = 'E' where Src_Proof_Id like 'YBQXINT'||:1"
                        self.oracle_execute(sql_update, pm)
                        Logsql.log("databaseLogger").debug(
                            self.database + " purchase_apply haidian update success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            self.database + " update-error:%s", e
                        )

    """
    wms 回写 海典系统
    """

    def wms_write_back(self, oper_sqlstr, oper_task_sqlstr, state_sql_str, new_haidian):
        for i in self.param_list:
            pm = {":1": i}
            mylist1 = self.oracle_select(oper_task_sqlstr, pm)
            # print(oper_sqlstr)
            Logsql.log("databaseLogger").debug(
                self.database + " wms_write_back oper_task_number: " + str(mylist1)
            )
            if mylist1:
                for i in range(0, len(mylist1)):
                    datalist1 = list(mylist1[i])
                    # 找到列表中的 datetime.datetime
                    for j in range(len(datalist1)):
                        if type(datalist1[j]) == datetime:
                            datalist1[
                                j
                            ] = "to_date('%s','yyyy-MM-dd hh24:mi:ss')" % datalist1[
                                j
                            ].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        if datalist1[j] == "C" or datalist1[j] == "E":
                            datalist1[j] = "0"
                    datalast = []
                    datalast.append(tuple(datalist1))
                    # 组装插入语句
                    sql1 = (
                        "INSERT into wmsoperate_task@wms VALUES %r" % tuple(datalast)
                    ).replace("None", "null")

                    # 正则表达式 去除sql中 日期两端的 双引号
                    self.oper_task_sqlstr = re.sub('"', "", sql1)
                    # print(self.oper_task_sqlstr)
                    try:
                        new_haidian.cur.execute(self.oper_task_sqlstr)
                        # new_haidian.conn.commit()
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back Wmsoperate_task insert success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back  Wmsoperate_task insert-error:%s",
                            e,
                        )
                    try:
                        sql_update = "update Operate_Task_Log set upd_state = 'E' where Src_Proof_Id like '%'||:1"
                        self.oracle_execute(sql_update, pm)
                        Logsql.log("databaseLogger").debug(
                            self.database
                            + " wms_write_back Operate_Task_Log update success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            self.database + " wms_write_back update-error:%s", e
                        )
            time.sleep(10)
            mylist2 = self.oracle_select(oper_sqlstr, pm)
            # print(oper_sqlstr)
            Logsql.log("databaseLogger").debug(
                self.database + " oper_number: " + str(mylist2)
            )
            if mylist2:
                for i in range(0, len(mylist2)):
                    datalist1 = list(mylist2[i])
                    # 找到列表中的 datetime.datetime
                    for j in range(len(datalist1)):
                        if type(datalist1[j]) == datetime:
                            datalist1[
                                j
                            ] = "to_date('%s','yyyy-MM-dd hh24:mi:ss')" % datalist1[
                                j
                            ].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        if datalist1[j] == "C" or datalist1[j] == "E":
                            datalist1[j] = "0"
                    datalast = []
                    datalast.append(tuple(datalist1))
                    # 组装插入语句
                    sql1 = (
                        "INSERT INTO Wmsoperate@Wms VALUES %r" % tuple(datalast)
                    ).replace("None", "null")

                    # 正则表达式 去除sql中 日期两端的 双引号
                    self.oper_sqlstr = re.sub('"', "", sql1)
                    # print(self.oper_sqlstr)
                    try:
                        new_haidian.cur.execute(self.oper_sqlstr)
                        # new_haidian.conn.commit()
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back  Wmsoperate insert success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back Wmsoperate insert-error:%s",
                            e,
                        )
                    try:
                        sql_update = "update Operate_Log set upd_state = 'E' where Src_Proof_Id like '%'||:1"
                        self.oracle_execute(sql_update, pm)
                        Logsql.log("databaseLogger").debug(
                            self.database + " wms_write_back Operate_Log update success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            self.database
                            + " wms_write_back Operate_Log update-error:%s",
                            e,
                        )
            mylist3 = self.oracle_select(state_sql_str, pm)
            # print(oper_sqlstr)
            Logsql.log("databaseLogger").debug(
                self.database + " wms_write_back state_number: " + str(mylist3)
            )
            if mylist3:
                for i in range(0, len(mylist3)):
                    datalist1 = list(mylist3[i])
                    # 找到列表中的 datetime.datetime
                    for j in range(len(datalist1)):
                        if type(datalist1[j]) == datetime:
                            datalist1[
                                j
                            ] = "to_date('%s','yyyy-MM-dd hh24:mi:ss')" % datalist1[
                                j
                            ].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        if datalist1[j] == "C" or datalist1[j] == "E":
                            datalist1[j] = "0"
                    datalast = []
                    datalast.append(tuple(datalist1))
                    # 组装插入语句
                    sql1 = (
                        "INSERT INTO wmsorderstate@Wms VALUES %r" % tuple(datalast)
                    ).replace("None", "null")

                    # 正则表达式 去除sql中 日期两端的 双引号
                    self.state_sqlstr = re.sub('"', "", sql1)
                    # print(self.state_sqlstr)
                    try:
                        new_haidian.cur.execute(self.state_sqlstr)
                        new_haidian.conn.commit()
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back wmsorderstate insert success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back  wmsorderstate insert-error:%s",
                            e,
                        )


    def wms_state_write_back(self,state_sql_str,new_haidian):
        for i in self.param_list:
            pm = {":1": i}
            mylist3 = self.oracle_select(state_sql_str, pm)
            # print(oper_sqlstr)
            Logsql.log("databaseLogger").debug(
                self.database + " wms_state_write_back state_number: " + str(mylist3)
            )
            if mylist3:
                for i in range(0, len(mylist3)):
                    datalist1 = list(mylist3[i])
                    # 找到列表中的 datetime.datetime
                    for j in range(len(datalist1)):
                        if type(datalist1[j]) == datetime:
                            datalist1[
                                j
                            ] = "to_date('%s','yyyy-MM-dd hh24:mi:ss')" % datalist1[
                                j
                            ].strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        if datalist1[j] == "C" or datalist1[j] == "E":
                            datalist1[j] = "0"
                    datalast = []
                    datalast.append(tuple(datalist1))
                    # 组装插入语句
                    sql1 = (
                        "INSERT INTO wmsorderstate@Wms VALUES %r" % tuple(datalast)
                    ).replace("None", "null")

                    # 正则表达式 去除sql中 日期两端的 双引号
                    self.state_sqlstr = re.sub('"', "", sql1)
                    print(self.state_sqlstr)
                    try:
                        new_haidian.cur.execute(self.state_sqlstr)
                        new_haidian.conn.commit()
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back wmsorderstate insert success"
                        )
                    except Exception as e:
                        Logsql.log("databaseLogger").debug(
                            new_haidian.database
                            + " wms_write_back  wmsorderstate insert-error:%s",
                            e,
                        )