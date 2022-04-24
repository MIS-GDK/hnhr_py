import logging
import logging.handlers
import time
import cx_Oracle
import re
from basic_oracle import *

if __name__ == "__main__":
    # 配送申请单 海典传到wms
    new_haidian = oracleCode("haidian", ["122110140000791"])
    new_wms = oracleCode("wms", [])
    new_haidian.oracle_conn()
    new_wms.oracle_conn()
    # 将数据 插入到wms数据库 并且 更新 海典 配送申请单upd_state状态 为'E'
    new_haidian.delivery_apply(new_haidian.delivery_sqlstr, new_wms)
    new_haidian.oracle_close()
    new_wms.oracle_close()