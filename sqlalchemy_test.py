# import cx_Oracle
# import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db = create_engine("oracle://hrhnprod:Ww7v*SLuhrDJ@192.168.0.190:1525/HRHNDB")

Base = declarative_base()


class bms_sa_doc1(Base):
    __tablename__ = "bms_sa_doc"
    salesid = Column("salesid", Integer, primary_key=True)
    customname = Column("customname", String)
    customid = Column("customid", String)


engine = create_engine("oracle://hrhnprod:Ww7v*SLuhrDJ@192.168.0.190:1525/HRHNDB")
# engine = create_engine(
#     "oracle://hrhnprod:Ww7v*SLuhrDJ@192.168.0.190:1525/HRHNDB", echo=True
# )
Database = sessionmaker(bind=engine)

if __name__ == "__main__":
    db = Database()
    query = db.query(bms_sa_doc1).filter(bms_sa_doc1.salesid == 327)
    print(query.count())
    query = query.all()
    print(type(query))
    for x in query:
        print(x.salesid, x.customid, x.customname)
