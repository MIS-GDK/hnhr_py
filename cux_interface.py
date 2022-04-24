import cx_Oracle

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.orm import sessionmaker


# declaractive用来表示类与表的关系。
Base = declarative_base()

# 创建表结构类：
# 一个表结构类必须包含一个__tablename__和primary_key的字段


class Cux_Ap_Req(Base):
    __tablename__ = "cux_29_ap_req_iface"
    request_id = Column("request_id", Integer)
    source_system_code = Column("source_system_code", VARCHAR(20))
    process_status = Column("process_status", VARCHAR(10))
    error_msg = Column("error_msg", VARCHAR(2000))
    pay_doc_num = Column("pay_doc_num", VARCHAR(50))
    invoice_num = Column("invoice_num", VARCHAR(50))
    __mapper_args__ = {
        "primary_key": [
            source_system_code,
            request_id,
        ]
    }


if __name__ == "__main__":
    engine = create_engine(
        "oracle+cx_oracle://erpdatainput:j7OPm0%v6MXPSQoF@10.0.119.46:1521/HADB1"
    )
    """
    创建DBSession类型:
    """
    DBSession = sessionmaker(bind=engine)
    """
    创建session对象:
    """
    sess = DBSession()
    query = sess.query(Cux_Ap_Req).filter(Cux_Ap_Req.process_status == "E")
    query2 = query.all()
    for x in query2:
        print(x.pay_doc_num, x.invoice_num, x.process_status)
