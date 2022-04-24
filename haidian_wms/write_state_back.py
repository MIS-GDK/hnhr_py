import logging
import logging.handlers
from basic_oracle import *


if __name__ == "__main__":
    # wms 传到海典
    new_wms = oracleCode("wms", ["122110200000136"])
    new_haidian = oracleCode("haidian", [])
    new_wms.oracle_conn()
    new_haidian.oracle_conn()
    # 将 wms Operate_Log 回写到海典wmsoperate 并且 更新 wms upd_state状态 为'E'
    new_wms.wms_state_write_back(new_wms.state_sqlstr, new_haidian)
    new_haidian.oracle_close()
    new_wms.oracle_close()