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


df = pandas.read_csv("C:/Users/Administrator/Desktop/2.txt", sep="\t", encoding="utf-8")


# dtyp = set_d_type_dict(df)

# pf = df.iloc[:, [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
# print(df)
dfl = df.iloc[:, 0:2]
# print(dfl)
# pd.concat([df, pd.DataFrame(columns=list('DE'))])
# dfl = pandas.concat([dfl, pandas.DataFrame(columns=["year", "month"])])
# dfl["year"] = ["2022"] * 40
# print(dfl)

# dfl2 = pandas.DataFrame()
dfl3 = pandas.DataFrame(
    None, columns=["deptid", "deptname", "year", "month", "year_plan", "month_plan"]
)
for i in range(2):
    dfl2 = pandas.DataFrame(
        None, columns=["deptid", "deptname", "year", "month", "year_plan", "month_plan"]
    )
    a = dfl.loc[i]
    d = pandas.DataFrame(a).T
    dfl2 = dfl2.append([d] * 12)
    dfl2["year"] = [
        "2022",
    ] * 12

    dfl2["month"] = [
        "2022-01",
        "2022-02",
        "2022-03",
        "2022-04",
        "2022-05",
        "2022-06",
        "2022-07",
        "2022-08",
        "2022-09",
        "2022-10",
        "2022-11",
        "2022-12",
    ]
    dfl2["year_plan"] = df.iloc[i, 2]
    df3 = df.iloc[i, 3:]
    dfl2["month_plan"] = df3.values
    print(dfl2)
    dfl3.append(dfl2)
    # print([pandas.Series([df.iloc(i, 2)] * 12)])
    # c = pandas.DataFrame(df[:, :]).T
    # print(c)
    # dfl2 = pandas.concat([dfl2, pandas.Series([d] * 12)])
    # print(dfl2)

# # print(dfl2)
dfl3 = dfl3.infer_objects()
# print(dfl2.dtypes)
dtyp = set_d_type_dict(dfl3)
print(dfl3)

# engine = create_engine("oracle://hrhnprod:9bcPa4hr16HN@192.168.0.43:1525/HRHNDB")
# # dfl2.to_sql(
# #     "dc_customer_budget_tl_1023",
# #     con=engine,
# #     if_exists="append",
# #     index=False,
# #     index_label=None,
# #     dtype=dtyp,
# # )

# """
# 创建对象的基类:
# """
# Base = declarative_base()
# """
# 定义User对象:
# """


# class Dc(Base):
#     # 表的名字:
#     __tablename__ = "area_dept_sales_plan_tl"

#     # 表的结构:
#     id = Column(NUMBER(20))
#     SALESDEPTNAME1 = Column(VARCHAR2(100))
#     SALESDEPTID2 = Column(NUMBER(20))
#     SALESDEPTNAME2 = Column(VARCHAR2(100))
#     YEAR = Column(VARCHAR2(4))
#     month = Column(VARCHAR2(7))
#     YEAR_PLAN = Column(NUMBER(20, 2))
#     MONTH_PLAN = Column(NUMBER(20, 2))

#     __mapper_args__ = {
#         "primary_key": [
#             SALESDEPTID2,
#             month,
#         ]
#     }
#     # 方法一，该方法直接获取数据库原始数值,对于一些特殊字符如时间戳无法转换
#     def to_dict(self):
#         # 记得加None(网上一些教程没有加None是无法使用的)
#         return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


# """
# 创建DBSession类型:
# """
# DBSession = sessionmaker(bind=engine)
# """
# 创建session对象:
# """
# session = DBSession()

# df_budget = df.iloc[:, 2:]
# df_budget_array = numpy.array(df_budget)  # 先将数据框转换为数组

# # train_data_list = train_data.tolist()  # 其次转换为列表
# # print(df_budget_array[0][11])  # 以数组形式打出来方便看
# i = 0
# j = 0
# for index, row in dfl2.iterrows():
#     # print(row)
#     dc = session.query(Dc).filter(Dc.customid == row[0], Dc.month == row[4]).one()
#     dc.month_budget = df_budget_array[i][j]
#     dc.class_code = 3
#     j = j + 1
#     if j == 12:
#         i = i + 1
#         j = 0

# session.commit()
# # 关闭session:
# session.close()
# # dc = session.query(Dc).filter(Dc.customid == 1005636,Dc.month == '2020-01').one()
# # dc = session.query(Dc).all()
# # print([v.to_dict() for v in dc])
# # 关闭引擎
# engine.dispose()
