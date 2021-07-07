from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    ForeignKey,
)

import cx_Oracle
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "oracle+cx_oracle://tplprod:tU:oeMKCo^>L,xK40@192.168.0.40:1521/HRHNDB",
    max_identifier_length=128,
    # echo=True, #echo参数为True时，会显示每条执行的SQL语句，可以关闭
)

Base = declarative_base()


class Orders(Base):
    # 必须对应数据库的表名
    __tablename__ = "pl_order_center_dtl"
    id = Column(String, primary_key=True)
    billno = Column(String)
    pihao = Column(String)
    pici = Column(String)
    goodsdesc = Column(String)
    goodsid = Column(String)
    quantity = Column(Integer)
    deleted = Column(String)

    # def __init__(self, id, billno, pihao, goodsid, quantity):
    #     self.id = id
    #     self.billno = billno
    #     self.pihao = pihao
    #     self.goodsid = goodsid
    #     self.quantity = quantity


class Goods(Base):
    # 必须对应数据库的表名
    __tablename__ = "pl_goodsinfo"
    id = Column(String, primary_key=True)
    goodsname = Column(String)


# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()

# add_order = Order(1111111111111111,"1111111111111111", 11111)
# session.add(add_order)
# session.commit()
orderlist = ["202103196109"]
for myorder in orderlist:
    Order = (
        session.query(Orders).filter_by(billno=myorder, pici=None, deleted="0").all()
    )
    goods = session.query
    for i in Order:
        goods = session.query(Goods).filter_by(id=i.goodsid).all()
        print(i.billno, i.pihao, goods[0].goodsname, i.quantity)
        # for j in goods:
        #     print(i.billno, j.goodsname, i.quantity)
