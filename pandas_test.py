import pandas
import numpy
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
        if "object" in str(j):
            type_dict.update({i: VARCHAR(512)})
        if "float" in str(j):
            type_dict.update({i: Integer()})
        if "int" in str(j):
            type_dict.update({i: Integer()})
    return type_dict


df = pandas.read_csv("C:/Users/Administrator/Desktop/1.txt", sep=",", encoding="utf-8")


# dtyp = set_d_type_dict(df)

# pf = df.iloc[:, [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
print(df)
dfl = df.iloc[:, 0:3]
# print(dfl)
# pd.concat([df, pd.DataFrame(columns=list('DE'))])
# dfl = pandas.concat([dfl, pandas.DataFrame(columns=["year", "month"])])
dfl["year"] = ["2020"] * 50
# print(dfl)
dfl2 = pandas.DataFrame()

for i in range(len(dfl)):
    a = dfl.loc[i]
    d = pandas.DataFrame(a).T
    dfl2 = dfl2.append([d] * 12)

dfl2["month"] = [
    "2020-01",
    "2020-02",
    "2020-03",
    "2020-04",
    "2020-05",
    "2020-06",
    "2020-07",
    "2020-08",
    "2020-09",
    "2020-10",
    "2020-11",
    "2020-12",
] * 50
print(dfl2)
dfl2 = dfl2.infer_objects()
print(dfl2.dtypes)
dtyp = set_d_type_dict(dfl2)


engine = create_engine("oracle://hrhnprod:9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")
# dfl2.to_sql(
#     "dc_customer_budget_tl_1023",
#     con=engine,
#     if_exists="append",
#     index=False,
#     index_label=None,
#     dtype=dtyp,
# )

"""
创建对象的基类:
"""
Base = declarative_base()
"""
定义User对象:
"""


class Dc(Base):
    # 表的名字:
    __tablename__ = "dc_customer_budget_tl_1023"

    # 表的结构:
    customid = Column(NUMBER(20))
    customname = Column(VARCHAR2(100))
    year = Column(VARCHAR2(4))
    month = Column(VARCHAR2(7))
    year_budget = Column(NUMBER(20, 2))
    month_budget = Column(NUMBER(20, 2))
    class_code = Column(NUMBER(2))

    __mapper_args__ = {
        "primary_key": [
            customid,
            month,
        ]
    }
    # 方法一，该方法直接获取数据库原始数值,对于一些特殊字符如时间戳无法转换
    def to_dict(self):
        # 记得加None(网上一些教程没有加None是无法使用的)
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


"""
创建DBSession类型:
"""
DBSession = sessionmaker(bind=engine)
"""
创建session对象:
"""
session = DBSession()

df_budget = df.iloc[:, 3:]
print(df_budget.iloc[0, 0])
df_budget_array = numpy.array(df_budget)  # 先将数据框转换为数组
# train_data_list = train_data.tolist()  # 其次转换为列表
# print(df_budget_array[0][11])  # 以数组形式打出来方便看
i = 0
j = 0
for index, row in dfl2.iterrows():
    print(row)
    dc = session.query(Dc).filter(Dc.customid == row[0], Dc.month == row[4]).one()
    dc.month_budget = df_budget_array[i][j]
    dc.class_code = 3
    j = j + 1
    if j == 12:
        i = i + 1
        j = 0

session.commit()
# 关闭session:
session.close()
# dc = session.query(Dc).filter(Dc.customid == 1005636,Dc.month == '2020-01').one()
# dc = session.query(Dc).all()
# print([v.to_dict() for v in dc])
# 关闭引擎
engine.dispose()
