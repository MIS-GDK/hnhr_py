import pandas
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, create_engine
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.orm import sessionmaker
from dateutil.relativedelta import relativedelta
from datetime import datetime

df = pandas.read_excel("C:/Users/Administrator/Desktop/2021重点客户.xls", sheet_name="分销部")

engine = create_engine("oracle://hrhnprod:9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")

Database = sessionmaker(bind=engine)
db = Database()

# declaractive用来表示类与表的关系。    
Base = declarative_base()

# 创建表结构类：
# 一个表结构类必须包含一个__tablename__和primary_key的字段


class customer(Base):
    __tablename__ = "pub_customer"
    customid = Column("customid", Integer, primary_key=True)
    customno = Column("customno", VARCHAR(40))
    customname = Column("customname", VARCHAR(100))


# print(df)
df["customid"] = ""
df["year"] = "2021"
df["class_code"] = 6
txt = "2020-12"
date1 = datetime.strptime(txt, "%Y-%m")
count = 1


for index, row in df.iterrows():
    if count <= 12:
        date1 = date1 + relativedelta(months=+1)
        date1 = date1.strftime("%Y-%m")
    else:
        count = 1
        date1 = datetime.strptime(txt, "%Y-%m")
        date1 = date1 + relativedelta(months=+1)
        date1 = date1.strftime("%Y-%m")

    res = db.query(customer).filter(customer.customno == row[0]).all()
    df.iloc[index, 5] = res[0].customid
    df.iloc[index, 2] = date1
    date1 = datetime.strptime(date1, "%Y-%m")
    count = count + 1

df = df[
    [
        "customid",
        "customname",
        "year",
        "month",
        "year_budget",
        "month_budget",
        "class_code",
    ]
]

df["customid"] = df["customid"].astype("int64")

df.to_sql(
    "dc_customer_budget_tl",
    con=engine,
    if_exists="append",
    index=False,
    index_label=None,
    # dtype=df.dtypes,
)
# 关闭引擎
engine.dispose()
