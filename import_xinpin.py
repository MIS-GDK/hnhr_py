import cx_Oracle
import numpy
import pandas

# from pandas import Series, DataFrame
from sqlalchemy import Column, create_engine, types

# 导入支持postgres的数据类型
from sqlalchemy.dialects.postgresql import NUMERIC, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import VARCHAR, Integer


def set_d_type_dict(df):
    type_dict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            type_dict.update({i: VARCHAR(512)})
        if "float" in str(j):
            type_dict.update({i: NUMERIC(20, 2)})
        if "int" in str(j):
            type_dict.update({i: Integer()})
    return type_dict


df = pandas.read_csv("C:/Users/Administrator/Desktop/3.txt", sep="\t", encoding="utf-8")

print(df.columns)
print(df.dtypes)
dtyp = set_d_type_dict(df)


engine = create_engine(
    "postgresql://gysxt_user20200513:?)&FL|<D,!*+\CS<X2ab)@192.168.0.230:21539/gysxt_data_20200513"
)

df.to_sql(
    "gdk_custom_zq_tl",
    con=engine,
    if_exists="replace",
    index=False,
    index_label=None,
    dtype=dtyp,
)

# 关闭引擎
engine.dispose()
