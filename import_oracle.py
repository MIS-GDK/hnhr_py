import logging
import pandas as pd
from sqlalchemy import create_engine, text

from sqlalchemy.types import VARCHAR, Integer, DECIMAL, NUMERIC
from sqlalchemy.dialects.oracle import VARCHAR2, NUMBER
from sqlalchemy.exc import SQLAlchemyError

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_data_types(df):
    """
    根据DataFrame的数据类型生成数据类型映射
    """
    type_dict = {}
    for col, dtype in df.items():
        if "object" in str(dtype):
            # 将VARCHAR2长度减小，避免超出Oracle限制
            max_length = df[col].str.len().max()
            if pd.isna(max_length):
                max_length = 100
            else:
                max_length = min(
                    int(max_length * 1.2), 4000
                )  # 给予20%的余量，但不超过4000
            type_dict[col] = VARCHAR2(max_length)
        if "object" in str(dtype):
            type_dict[col] = VARCHAR2(1000)
        elif "string" in str(dtype):
            type_dict[col] = VARCHAR2(1000)
        elif "float" in str(dtype):
            type_dict[col] = NUMBER(38, 2)
        elif "int" in str(dtype):
            type_dict[col] = NUMBER(38)
    return type_dict


def import_to_database(file_path, table_name, connection_string, chunk_size=10000):
    """
    将数据导入数据库

    Parameters:
    - file_path: 数据文件路径
    - table_name: 目标表名
    - connection_string: 数据库连接字符串
    - chunk_size: 分批导入的大小
    """
    engine = None
    try:
        # 读取数据文件
        logging.info(f"开始读取文件: {file_path}")
        df = pd.read_csv(file_path, sep="\t", encoding="utf-8")

        logging.info(f"成功读取 {len(df)} 行数据")

        # 获取数据类型映射
        dtype_dict = get_data_types(df)

        # 创建数据库连接
        engine = create_engine(connection_string, pool_recycle=3600)

        # 分批写入数据
        with engine.begin() as connection:
            df.to_sql(
                table_name,
                con=connection,
                if_exists="replace",
                index=False,
                dtype=dtype_dict,
                chunksize=chunk_size,
            )

            # 验证导入结果
            result = connection.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar()

            logging.info(f"成功导入 {result} 行数据到表 {table_name}")

        return True, f"成功导入 {result} 行数据"

    except FileNotFoundError as e:
        logging.error(f"文件不存在: {file_path}")
        return False, "文件不存在"
    except pd.errors.EmptyDataError:
        logging.error("文件为空")
        return False, "文件为空"
    except SQLAlchemyError as e:
        logging.error(f"数据库错误: {str(e)}")
        return False, f"数据库错误: {str(e)}"
    except Exception as e:
        logging.error(f"未预期的错误: {str(e)}")
        return False, f"未预期的错误: {str(e)}"
    finally:
        if engine:
            engine.dispose()
            logging.info("数据库连接已关闭")


if __name__ == "__main__":
    # 数据库连接配置
    CONNECTION_STRING = "oracle+cx_oracle://hrhnprod:9bcPa4hr16HN@SUPPLYCHAIN"
    # CONNECTION_STRING ="oracle://hrhnprod:9bcPa4hr16HN@192.168.0.43:1525/HRHNDB"

    # 执行导入
    success, message = import_to_database(
        file_path="C:/Users/Administrator/Desktop/2.txt",
        table_name="gdk_temp_tl",
        connection_string=CONNECTION_STRING,
    )

    if success:
        logging.info(message)
    else:
        logging.error(message)
