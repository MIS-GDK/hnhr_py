from operator import index
from sqlalchemy.types import Integer, VARCHAR
import cx_Oracle
import pandas as pd
from sqlalchemy import create_engine, types, Column

# 导入支持oracle的数据类型
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2
import re

# engine = create_engine("oracle+cx_oracle://hrhnprod:9bcPa4hr16HN@SUPPLYCHAIN")
# engine = create_engine(
#     "oracle+cx_oracle://wmsinterface:T#ClzR74WuLPIZ1c@192.168.0.43:1525/hrhndb"
# )
engine = create_engine(
    "oracle+cx_oracle://QUERY_HEN:AMm1!%KE7kmees09@10.0.0.201:1521/?service_name=bjdb"
)
sql1 = """
SELECT DISTINCT a.Objbusno "机构编码",
                (SELECT s_Busi.Orgname
                   FROM s_Busi
                  WHERE s_Busi.Busno = a.Objbusno) "机构名称",
                b.Wareid "商品id",
                e.Warecode "商品编码",
                e.Warename "商品名称",
                e.Warespec "商品规格"
  FROM t_Md_Notice_Accept_h a, t_Md_Notice_Accept_d b, v_Ware_Base e
 WHERE a.Billcode = 'MDACN'
   AND (a.Compid IN (SELECT Compid FROM s_Company WHERE Parentid = {compid}) OR
       a.Compid = {compid})
   AND (a.Execdate >= To_Date({date1}, 'yyyy-MM-dd'))
   AND (a.Execdate < To_Date({date2}, 'yyyy-MM-dd'))
   AND a.Acceptno = b.Acceptno
   AND b.Wareid = e.Wareid
   AND a.Compid = e.Compid
   AND NOT EXISTS
 (SELECT 1
          FROM t_Md_Notice_Accept_h c, t_Md_Notice_Accept_d d
         WHERE c.Acceptno = d.Acceptno
           AND c.Execdate < To_Date({date1}, 'yyyy-MM-dd')
           AND c.Billcode = 'MDACN'
           AND (c.Compid IN
               (SELECT Compid FROM s_Company WHERE Parentid = {compid}) OR
               c.Compid = {compid})
           AND d.Wareid = b.Wareid
           AND c.Objbusno = a.Objbusno)
 ORDER BY a.Objbusno
"""
# 参数生成
while True:
    compid = input("请输入机构ID:")
    if compid.isdigit():
        break
    else:
        print("输入机构ID不正确!")
        continue
regexp = r"\d{4}-\d{2}-\d{2}"
while True:
    date1 = input("请输入开始日期(包含):")
    if re.match(regexp, date1):
        break
    else:
        print("输入日期格式不正确!")
        continue

while True:
    date2 = input("请输入结束日期(不包含):")
    if re.match(regexp, date2):
        break
    else:
        print("输入日期格式不正确!")
        continue
info1 = {"compid": compid, "date1": "'" + date1 + "'", "date2": "'" + date2 + "'"}
sql1 = sql1.format(**info1)
# print(sql1)
sql2 = """
SELECT DISTINCT t_Accept_h.Busno "机构编码",
                (SELECT s_Busi.Orgname
                   FROM s_Busi
                  WHERE s_Busi.Busno = t_Accept_h.Busno) "机构名称",
                t_Accept_d.Wareid AS "商品id",
                t_Ware.Warecode AS "商品编码",
                t_Ware.Warename AS "商品名称",
                t_Ware.Warespec AS "商品规格"
  FROM t_Accept_d t_Accept_d
  JOIN t_Accept_h t_Accept_h
    ON t_Accept_d.Acceptno = t_Accept_h.Acceptno
  LEFT JOIN v_Ware t_Ware
    ON t_Accept_d.Wareid = t_Ware.Wareid
   AND t_Accept_h.Compid = t_Ware.Compid
 WHERE t_Accept_h.Billcode = 'ACC'
   AND (t_Accept_h.Compid IN
       (SELECT Compid FROM s_Company WHERE Parentid = {compid}) OR
       t_Accept_h.Compid = {compid})
   AND t_Accept_h.Execdate >= To_Date({date1}, 'yyyy-MM-dd')
   AND t_Accept_h.Execdate < To_Date({date2}, 'yyyy-MM-dd')
   AND NOT EXISTS
 (SELECT 1
          FROM t_Accept_d t_Accept_D2
          JOIN t_Accept_h t_Accept_h
            ON t_Accept_D2.Acceptno = t_Accept_h.Acceptno
         WHERE t_Accept_h.Billcode = 'ACC'
           AND (t_Accept_h.Compid IN
               (SELECT Compid FROM s_Company WHERE Parentid = {compid}) OR
               t_Accept_h.Compid = {compid})
           AND (t_Accept_h.Execdate < To_Date({date1}, 'yyyy-MM-dd'))
           AND t_Accept_D2.Wareid = t_Accept_d.Wareid)
"""
sql2 = sql2.format(**info1)

address = r"C:\Users\Administrator\Desktop"
filename = compid + "首次购进.xlsx"

if compid == "2209":
    df1 = pd.read_sql_query(sql1, engine)
    df1.to_excel(address + "\\" + filename)
else:
    df2 = pd.read_sql_query(sql2, engine)
    df2.to_excel(address + "\\" + filename, index=False)
