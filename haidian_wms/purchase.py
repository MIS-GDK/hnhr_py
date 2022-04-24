import logging
import logging.handlers
import time
import cx_Oracle
import re
from basic_oracle import *


if __name__ == "__main__":
    # 采购订单 海典传到wms
    new_haidian = oracleCode("haidian", ["1221101100213", "1221101500341"])
    new_wms = oracleCode("wms", [])
    new_haidian.oracle_conn()
    new_wms.oracle_conn()
    # 采购订单 海典 传送到 wms,需要将中间库数据 写入到wms
    new_haidian.purchase_apply(new_haidian.purchase_sqlstr, new_wms)
    new_haidian.oracle_close()
    new_wms.oracle_close()