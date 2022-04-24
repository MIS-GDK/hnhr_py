import pandas
import numpy
import cx_Oracle
import pymssql
from sqlalchemy.types import Integer, VARCHAR

# from pandas import Series, DataFrame
from sqlalchemy import create_engine, types, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 导入支持oracle的数据类型
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2


def set_d_type_dict(df):
    type_dict = {}
    for i, j in zip(df.columns, df.dtypes):
        print(i, j)
        if "object" in str(j):
            type_dict.update({i: VARCHAR(512)})
        if "float" in str(j):
            type_dict.update({i: Integer()})
        if "int" in str(j):
            type_dict.update({i: Integer()})
    return type_dict


df = pandas.read_csv("C:/Users/Administrator/Desktop/1.txt", sep="\t", encoding="utf-8")


print(df.dtypes)
print(df.columns)


dtyp = set_d_type_dict(df)

engine = create_engine("oracle://hrhnprod:9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")
# #方法一
# engine = create_engine(
#     "oracle+cx_oracle://erpdatainput:j7OPm0%v6MXPSQoF@10.0.119.46:1521/HADB1"
# )

# engine = create_engine(
#     "mssql+pymssql://ysadmin:0wM71IakpU&1s&@192.168.0.16:1433/ysdata"
# )
# 方法二
# engine = create_engine("oracle+cx_oracle://erpdatainput:j7OPm0%v6MXPSQoF@ERP_SHENZ_46")
# engine = create_engine("oracle+cx_oracle://tplprod:tU:oeMKCo^>L,xK4@HRHNDB")
# #方法三
# ip = "10.0.119.46"
# port = "1521"
# uname = "erpdatainput"  # 用户名
# pwd = "j7OPm0%v6MXPSQoF"  # 密码
# tnsname = "hadb"  # 实例名
# dsnStr = cx_Oracle.makedsn(ip, port, service_name=tnsname)
# connect_str = "oracle://%s:%s@%s" % (uname, pwd, dsnStr)
# engine = create_engine(connect_str, pool_recycle=3600)


df.to_sql(
    "gdk_order_check3_tl",
    con=engine,
    if_exists="replace",
    index=False,
    index_label=None,
    dtype=dtyp,
)

# # 关闭引擎
engine.dispose()
